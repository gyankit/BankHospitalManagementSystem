from App import app, db
from flask import render_template, redirect, request, url_for, flash, session
from passlib.hash import sha256_crypt
from App.decorators import login_required, login_checked
from App.forms import LoginForm, AccountCreateForm, AccountDeleteForm
from App.models import UserStore
from datetime import datetime
import json


#Login route
@app.route('/')
@app.route('/index')
@app.route('/login', methods=['GET', 'POST'])
@login_checked
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = UserStore.query.filter_by(username=username).first()
        if user is None:
            flash('Wrong login credantials', 'danger')
        else:
            if sha256_crypt.verify(password, user.password):
                session['is_login'] = True
                session['user'] = username
                flash('Successful Login', 'success')
                return redirect(url_for('home'))
            else:
                flash('Wrong Password', 'danger')
            
    return render_template('login.html', form=form)

#Logout Route
@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('Successfully Logout', 'success')
    return redirect(url_for('login'))
    
#Home Route
@app.route('/home')
@login_required
def home():
    return render_template('home.html')

"""
#Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = sha256_crypt.hash(form.password.data)

        if UserStore.query.filter_by(username=username).first():
            flash('Username already Exists', 'danger')
        else:
            newUser = UserStore(username=username, password=password, datetime=datetime.now())
            db.session.add(newUser)
            db.session.commit()
            flash('New User Successfully Added', 'success')
            return redirect(url_for('home'))
            
    return render_template('register.html', form=form)
""" 

#Create Account Route
@app.route('/account/create')
@login_required
def accountCreate():
    form = AccountCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        CustomerId = form.customerId.data
        AccountType = form.cccountType.data
        AccountId = form.depositAmount.data
    return render_template('accountCreate.html', form=form)

#Delete Account Route
@app.route('/account/delete')
@login_required
def accountDelete():
    form = AccountDeleteForm()
    if request.method == 'POST' and form.validate_on_submit():
        AccountId = form.accountId.data
        AccountType = form.accountType.data
    return render_template('accountDelete.html', form=form)

#Account Status Route
@app.route('/account')
@app.route('/account/status')
@login_required
def accountStatus():
    return render_template('accountStatus.html')
