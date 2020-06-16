from App import app, db
from flask import render_template, redirect, request, url_for, flash, session, jsonify
from passlib.hash import sha256_crypt
from App.decorators import login_required, login_checked
from App.forms import LoginForm, CustomerForm, AccountCreateForm, AccountDeleteForm
from App.models import UserStore, Customer
from App.cities import getstates, getcities
from datetime import datetime
import json
from App.cities import getstates, getcities


#Login route
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

#Logout Route
@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('Successfully Logout', 'success')
    return redirect(url_for('login'))
    
#Home Route
@app.route('/')
@app.route('/home')
@login_required
def home():
    return render_template('home.html')


#City Route
@app.route('/city/<state>')
@login_required
def city(state):
    cities = getcities()[int(state)]
    cityArray = []
    for city in cities:
        cityObj = {}
        cityObj['id'] = city[0]
        cityObj['name'] = city[1]
        cityArray.append(cityObj)
    return jsonify({'cities' : cityArray})

#Customer Route
@app.route('/customer/create', methods=['GET', 'POST'])
@login_required
def customerCreate():
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
    return render_template('customerCreate.html', form=form)

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