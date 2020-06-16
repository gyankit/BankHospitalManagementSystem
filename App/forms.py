from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, SubmitField, BooleanField, IntegerField, SelectField, DecimalField

class LoginForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    submit = SubmitField('Login')


class AccountCreateForm(FlaskForm):
    CustomerId = IntegerField('Customer Id', [validators.DataRequired()])
    AccountType = SelectField('Account Type',[validators.DataRequired()], choices=[('savings', 'Saving Account'),('current', 'Current Account')])
    DepositAmount = DecimalField('Deposit Amount', [validators.DataRequired()])
    submit = SubmitField('Create Account')

    
class AccountDeleteForm(FlaskForm):
    AccountId = IntegerField('Account Id', [validators.DataRequired()])
    AccountType = SelectField('Account Type',[validators.DataRequired()], choices=[('savings', 'Saving Account'),('current', 'Current Account')])
    submit = SubmitField('Delete Account')



    
