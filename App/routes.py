from App import app, db
from flask import render_template, redirect, request, url_for, flash, session
from passlib.hash import sha256_crypt
from App.forms import LoginForm, AccountCreateForm, AccountDeleteForm
from App.models import User
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
    


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/Account_create')
def Account_create():
    form = Account_createForm()
    if request.method == 'POST' and form.validate_on_submit():
        Customer_Id = form.form.Customer_Id.data
        Account_type = form.Account_type.data
        Account_Id = form.form.Deposit_Amount.data
    return render_template('Account_create.html',form=form)




@app.route('/Account_delete')
def Account_delete():
    form = Account_deleteForm()
    if request.method == 'POST' and form.validate_on_submit():
        Account_Id = form.form.Account_Id.data
        Account_type = form.Account_type.data
    return render_template('Account_delete.html',form=form)


@app.route('/Account_status')
def Account_status():
    return render_template('Account_status.html')
