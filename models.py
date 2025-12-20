from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(200))
    role = db.Column(db.String(10))

    address = db.Column(db.String(255))
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)

    def __repr__(self):
        return f"<User {self.email}>"
    
class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    image = db.Column(db.String(200))
    stock = db.Column(db.Boolean, default = True)

    # add stock column

    farmer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    farmer = db.relationship('User', backref='products')

    def __repr__(self):
        return f"<Product {self.name}>"