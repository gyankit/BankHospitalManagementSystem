from App import app, db
from flask import render_template, redirect, request, url_for, flash, session
from passlib.hash import sha256_crypt
from App.forms import LoginForm, Account_createForm,Account_deleteForm
from App.models import User
from datetime import datetime
import json


@app.route('/')
@app.route('/index')
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user=User.query.filter_by(username=username).first()
        if user is None:
            flash('Wrong login credantials', 'danger')
        else:
            if sha256_crypt.verify(password, user.password):
                flash('Successful Login', 'success')
                return redirect(url_for('home'))
            else:
                flash('Wrong Password', 'danger')
            
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.hash(form.password.data)

        if User.query.filter_by(email=email).first():
            flash('Email already Exists', 'danger')
        elif User.query.filter_by(username=username).first():
            flash('Username already Exists', 'danger')
        else:
            newUser = User(email=email, username=username, password=password, datetime=datetime.now())
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


