from flask_wtf import FlaskForm
from wtforms import BooleanField, DateField, IntegerField, PasswordField, RadioField, SelectField, StringField,SubmitField, validators
from App.cities import getstates

class NonValidatingSelectField(SelectField):
    def pre_validate(self, form):
        pass


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    rememberMe = BooleanField('Remember Me')
    submit = SubmitField('Login')


class CustomerSearchForm(FlaskForm):
    ssnId = StringField('SSN Id', [validators.optional(), validators.regexp('\d{9}$', message='SSN Id must have 9 digits')])
    customerId = StringField('Customer Id', [validators.optional(), validators.regexp('\d{9}$', message='Customer Id must have 9 digits')])
    submit = SubmitField('Search')


class CustomerCreateForm(FlaskForm):
    ssnid = StringField('Customer SSN Id', [
        validators.DataRequired(), validators.regexp('\d{9}$', message='SSN Id must have 9 digits')])
    customerName = StringField('Customer Name', [validators.DataRequired()])
    age = StringField('Age', [validators.DataRequired(), validators.regexp(
        '\d{1,3}$', message='Customer Age maximum have 3 digits')])
    state = SelectField('State', [validators.DataRequired()], choices=[(state,state) for state in getstates()])
    city = NonValidatingSelectField('City', [validators.DataRequired()], choices=[])
    submit = SubmitField('Submit')

class CustomerUpdateForm(FlaskForm):
    customerName = StringField('Customer New Name', [validators.optional()])
    age = StringField('Customer New Age', [validators.optional()])
    state = SelectField('State', [validators.optional()], choices=[(state,state) for state in getstates()])
    city = NonValidatingSelectField('City', [validators.optional()], choices=[])
    submit = SubmitField('Update Details')


class AccountCreateForm(FlaskForm):
    customerId = StringField('Customer Id', [validators.DataRequired(
    ), validators.regexp('\d{9}$', message='Customer Id must have 9 digit')])
    accountType = SelectField('Account Type', [validators.DataRequired()], choices=[('Savings', 'Saving Account'), ('Current', 'Current Account')])
    depositAmount = IntegerField('Deposit Amount', [validators.DataRequired()])
    submit = SubmitField('Submit')


class AccountSearchForm(FlaskForm):
    accountId = IntegerField('Account Id', [validators.optional()])
    customerId = IntegerField('Customer Id', [validators.optional()])
    submit = SubmitField('Search')


class DepositAmountForm(FlaskForm):
    amount = IntegerField('Deposit Amount', [validators.DataRequired()])
    submit = SubmitField('Deposit')


class WithDrawAmountForm(FlaskForm):
    amount = IntegerField('Withdraw Amount', [validators.DataRequired()])
    submit = SubmitField('Withdraw')


class TransferAmountForm(FlaskForm):
    sourceAccId = StringField('Source Account Id', [validators.DataRequired(), validators.regexp('\d{9}$', message='Account Id must have 9 digit')])
    targetAccId = StringField('Target Account Id', [validators.DataRequired(), validators.regexp('\d{9}$', message='Account Id must have 9 digit')])
    amount = IntegerField('Transfer Amount', [validators.DataRequired()])
    submit = SubmitField('Transfer')
