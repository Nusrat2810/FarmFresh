from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import FileField, SelectField, StringField,PasswordField,SubmitField,SearchField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

class RegistrationForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    role = SelectField('Role', choices=[('farmer', 'Farmer'), ('customer', 'Customer')], validators=[DataRequired()])
    submit = SubmitField('Register') #creates submit button in html


class LoginForm(FlaskForm):
    email = StringField('Email',  validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    quantity = StringField('Quantity', validators=[DataRequired()])
    image = FileField('Product Image', validators=[FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField('Add Product')

class EditProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address')
    password = PasswordField('Password (leave blank if unchanged)', validators=[Optional()])
    confirm_password = PasswordField('Confirm Password', validators=[Optional()])
    submit = SubmitField('Update Profile')
