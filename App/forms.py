from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, SubmitField, BooleanField, IntegerField, SelectField

class LoginForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    rememberMe = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    email = StringField('Email', [validators.DataRequired()])
    username = StringField('Username', [validators.DataRequired(), validators.length(min=5, max=15)])
    password = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match'), validators.length(min=8, max=25)])
    confirm = PasswordField('Confirm Password', [validators.DataRequired(), validators.length(min=8, max=25)])
    submit = SubmitField('Register')

class CustomerForm(FlaskForm):
	ssnid = IntegerField('Customer SSN Id', [validators.DataRequired(), validators.length(min=9, max=9)])
	customer_name = StringField('Customer Name', [validators.DataRequired()])
	age = IntegerField('Age', [validators.DataRequired()])
	address = StringField('Address', [validators.DataRequired()])
	state = SelectField('State', [validators.DataRequired()], choices=[])
	city = SelectField('City', [validators.DataRequired()], choices=[])
	submit = SubmitField('Submit')
