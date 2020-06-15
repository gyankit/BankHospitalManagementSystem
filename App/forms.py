from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, SubmitField, BooleanField,IntegerField,SelectField,DecimalField

class LoginForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    rememberMe = BooleanField('Remember Me')
    submit = SubmitField('Login')


class Account_createForm(FlaskForm):
    
    Customer_Id = IntegerField('Customer Id', [validators.DataRequired()])
    Account_Type = SelectField('Account Type',[validators.DataRequired()], choices=[('savings','Saving Account'),('current','Current Account')])
    Deposit_Amount = DecimalField('Deposit Amount', [validators.DataRequired()])
    submit = SubmitField('Create Account')



class Account_deleteForm(FlaskForm):
    
    Account_Id = IntegerField('Account Id', [validators.DataRequired()])
    Account_Type = SelectField('Account Type',[validators.DataRequired()], choices=[('savings','Saving Account'),('current','Current Account')])
    submit = SubmitField('Delete Account')



    