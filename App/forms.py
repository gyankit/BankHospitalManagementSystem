from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, SubmitField, BooleanField, IntegerField, SelectField, DecimalField

class LoginForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    rememberMe = BooleanField('Remember Me')
    submit = SubmitField('Login')


class CustomerForm(FlaskForm):
	ssnid = IntegerField('Customer SSN Id', [validators.DataRequired(), validators.length(min=9, max=9)])
	customer_name = StringField('Customer Name', [validators.DataRequired()])
	age = IntegerField('Age', [validators.DataRequired()])
	address = StringField('Address', [validators.DataRequired()])
	state = SelectField('State', [validators.DataRequired()], choices=[])
	city = SelectField('City', [validators.DataRequired()], choices=[])
	submit = SubmitField('Submit')


class AccountCreateForm(FlaskForm):
    customerId = IntegerField('Customer Id', [validators.DataRequired()])
    accountType = SelectField('Account Type',[validators.DataRequired()], choices=[('savings', 'Saving Account'),('current', 'Current Account')])
    depositAmount = DecimalField('Deposit Amount', [validators.DataRequired()])
    submit = SubmitField('Submit')


class AccountDeleteForm(FlaskForm):
    accountId = IntegerField('Account Id', [validators.DataRequired()])
    accountType = SelectField('Account Type',[validators.DataRequired()], choices=[('savings', 'Saving Account'),('current', 'Current Account')])
    submit = SubmitField('Delete Account')



    
