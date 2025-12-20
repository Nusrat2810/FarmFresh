from flask import Flask, render_template, redirect, url_for, flash, request
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from forms import RegistrationForm, LoginForm, ProductForm, ProfileForm

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'no-secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['UPLOAD_FOLDER'] = 'static/images'
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    from models import User, Product

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    if not os.path.exists('instance/database.db'):
        with app.app_context(): # gives flask access to app configuration
            db.create_all()
            print("Database Created!")

    @app.route('/') #test route
    def home():
        return render_template('base.html')
    

    @app.route('/register', methods=['GET','POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        
        form = RegistrationForm()
        if form.validate_on_submit():
            # check if user already exist
            existing_user = User.query.filter_by(email = form.email.data).first()
            if existing_user:
                flash('Email already exist', 'danger')
                return redirect(url_for('register'))
            
            #hashing password
            hashed_password = generate_password_hash(form.password.data)

            #create user

            new_user = User(
                name = form.name.data,
                email = form.email.data,
                password = hashed_password,
                role = form.role.data
            )

            db.session.add(new_user)
            db.session.commit()

            print(User.query.all())
            #to check if account was created

            flash('Registration Successful!', 'success')
            return redirect(url_for('login'))
        
        return render_template('register.html', form=form)
    

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        #if request.method == 'POST':
        if current_user.is_authenticated:
            return redirect(url_for('home'))

        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and check_password_hash(user.password, form.password.data):
                login_user(user)
                flash(f'Welcome, {user.name}!', 'success')

                # Role-based redirect
                if user.role == 'customer':
                    return redirect(url_for('dashboard'))
                else:
                    return redirect(url_for('products'))
            else:
                flash('Login failed. Check email and password.', 'danger')

        return render_template('login.html', form=form)
    
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('home'))
    
    
    @app.route('/products', methods = ['GET','POST'])
    @login_required
    def products():
        if current_user.role != 'farmer':
            flash('Unauthorized access', 'danger')
            return redirect(url_for('home'))
        
        form = ProductForm()

        if request.method == 'POST':
            if form.validate_on_submit():
                filename = None

                if form.image.data:
                    filename = secure_filename(form.image.data.filename)
                    form.image.data.save(
                        os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    )

                product = Product(
                    name = form.name.data,
                    price = float(form.price.data),
                    quantity = int(form.quantity.data),
                    image = filename,
                    farmer_id = current_user.id
                    
                )

                db.session.add(product)
                db.session.commit()
                print(Product.query.all())

                flash('Product added!', 'success')
                return redirect(url_for('products'))
        products = Product.query.filter_by(farmer_id=current_user.id).all()
        
        return render_template('products.html', form=form, products=products)
    
    @app.route('/delete_product<int:product_id>', methods = ['POST'])
    @login_required
    def delete_product(product_id):

        product = Product.query.get_or_404(product_id)
        if current_user.role != 'farmer':
            flash('Unauthorized access', 'danger')
            return redirect(url_for('home'))
        
        db.session.delete(product)
        db.session.commit()
        flash(f"{product.name} has been deleted.", "success")
        return redirect(url_for('products'))
        

    
    """@app.route('/add_product', methods=['GET','POST'])
    @login_required
    def add_product():
        if current_user.role != 'farmer':
            flash('Unauthorized access', 'danger')
            return redirect(url_for('home'))
        
        form = ProductForm()
        if form.validate_on_submit():
            filename = None

            if form.image.data:
                filename = secure_filename(form.image.data.filename)
                form.image.data.save(
                    os.path.join(app.config['UPLOAD_FOLDER'], filename)
                )

            product = Product(
                name = form.name.data,
                price = float(form.price.data),
                quantity = int(form.quantity.data),
                image = filename,
                farmer_id = current_user.id
            )

            db.session.add(product)
            db.session.commit()
            print(Product.query.all())

            flash('Product added!', 'success')
            return redirect(url_for('products'))
        
        return render_template('products.html', form=form)"""

    @app.route('/dashboard')
    @login_required
    def dashboard():
        farmers_db = User.query.filter_by(role='farmer').all()
        farmers = []
        for f in farmers_db:
            if f.lat is not None and f.lon is not None:
                farmers.append({
                    "name" : f.name,
                    "address" : f.address,
                    "lat" : f.lat,
                    "lon" : f.lon
                })

        products = Product.query.all()

        return render_template('dashboard.html', farmers = farmers, products = products)
    
    @app.route('/profile', methods = ['GET', 'POST'])
    @login_required
    def profile():
        if current_user.role != 'farmer':
            flash('Unauthorized access', 'danger')
            return redirect(url_for('home'))
        
        form = ProfileForm()
        
        """if request.method == 'POST':
            return 
        
        else:
            return"""
        

        if form.validate_on_submit():
            # Convert address → latitude & longitude
            lat, lon = geocode_address(form.address.data)
            if lat is None:
                flash('Could not locate address. Please enter more details.', 'danger')
                return redirect(url_for('profile'))
            
            current_user.address = address
            current_user.latitude = lat
            current_user.longitude = lon
            db.session.commit()  # Saves changes permanently

            flash('Farm location saved successfully!', 'success')
            return redirect(url_for('products'))
            
        

        return render_template('profile.html')
    
    def geocode_address(address):
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": address,
            "format": "json"
        }
        headers = {"User-Agent": "FarmFreshApp"}  # required by Nominatim

        response = requests.get(url, params=params, headers=headers)
        data = response.json()

        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
        return None, None

    

    
    return app
