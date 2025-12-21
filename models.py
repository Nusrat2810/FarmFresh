from app import db
from flask_login import UserMixin
from datetime import datetime

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
    farmer_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    farmer = db.relationship('User', backref='products')

    def __repr__(self):
        return f"<Product {self.name}>"
    

class Order(db.Model):

    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, default = datetime.utcnow)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id')) #name of the table products
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id')) #name of table users
    farmer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.String(20), default = 'pending')

    product = db.relationship('Product', backref = 'orders') #product new var, Product class name and orders table name
    buyer = db.relationship('User', foreign_keys=[buyer_id], backref='orders_placed') # User class name, buyer_id column name
    farmer = db.relationship('User', foreign_keys=[farmer_id], backref='orders_received')

    def __repr__(self):
        return f"<Order {self.id} - {self.status}>"