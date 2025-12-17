from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

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
    
    if not os.path.exists('database.db'):
        with app.app_context(): # gives flask access to app configuration
            db.create_all()
            print("Database Created!")

    @app.route('/') #test route
    def home():
        return "FarmFresh is running!"
    
    return app
