from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm, LoginForm

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'no-secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    from models import User

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
                if user.role == 'farmer':
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
    

    @app.route('/dashboard')
    @login_required
    def dashboard():
        return render_template('dashboard.html')
    
    @app.route('/products')
    @login_required
    def products():
        return render_template('products.html')
    
    @app.route('/add_product')
    @login_required
    def add_product():
        return render_template('products.html')




    
    return app
