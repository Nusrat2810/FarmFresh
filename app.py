from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'no-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

@app.route('/')
def home():
    return "FarmFresh is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000', debug=True)