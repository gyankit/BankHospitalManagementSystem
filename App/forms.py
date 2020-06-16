from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, SubmitField, BooleanField, IntegerField, SelectField, DecimalField


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    submit = SubmitField('Login')


class AccountCreateForm(FlaskForm):
    customerId = IntegerField('Customer Id', [validators.DataRequired()])
    accountType = SelectField('Account Type',[validators.DataRequired()], choices=[('savings', 'Saving Account'),('current', 'Current Account')])
    depositAmount = DecimalField('Deposit Amount', [validators.DataRequired()])
    submit = SubmitField('Submit')


class AccountDeleteForm(FlaskForm):
    accountId = IntegerField('Account Id', [validators.DataRequired()])
    accountType = SelectField('Account Type',[validators.DataRequired()], choices=[('savings', 'Saving Account'),('current', 'Current Account')])
    submit = SubmitField('Delete Account')



    
