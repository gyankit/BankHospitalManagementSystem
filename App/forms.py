from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, SubmitField, BooleanField

class LoginForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    rememberMe = BooleanField('Remember Me')
    submit = SubmitField('Login')