from App import app, db
from flask import render_template, redirect, request, url_for, flash, session, jsonify
from passlib.hash import sha256_crypt
from App.forms import LoginForm, RegisterForm, CustomerForm
from App.models import User, Customer
from datetime import datetime
import json
from App.cities import getstates, getcities

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
            flash('Wrong login credentials', 'danger')
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


@app.route('/city/<state>')
def city(state):
    cities = getcities()[int(state)]

    cityArray = []
    for city in cities:
        cityObj = {}
        cityObj['id'] = city[0]
        cityObj['name'] = city[1]
        cityArray.append(cityObj)

    return jsonify({'cities' : cityArray})


@app.route('/cust_scrn', methods=['GET', 'POST'])
def cust_scrn():
    form = CustomerForm()
    states = getstates()

    form.state.choices = [(i,state) for i,state in enumerate(states)]

    if request.method == 'POST' and form.validate_on_submit():
        ssnid = form.ssnid.data
        cust_name = form.customer_name.data
        age = form.age.data
        address = form.age.data
        state = form.state.data
        city = form.city.data

        if User.query.filter_by(ssnid=ssnid).first():
            flash('SSN Id already taken', 'danger')
        else:
            newCustomer = Customer(ssnid=ssnid, customer_name=cust_name, age=age, address=address, state=state, city=city)
            db.session.commit()
            flash('New Customr Successfully Added', 'success')
            return redirect(url_for('home'))

    return render_template('cust_scrn.html', form=form)