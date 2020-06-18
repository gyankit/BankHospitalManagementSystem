from App import app, db
from flask import render_template, redirect, request, url_for, flash, session, jsonify, abort
from passlib.hash import sha256_crypt
from App.decorators import *
from App.forms import *
from App.models import *
from App.cities import getstates, getcities
from datetime import datetime
from random import randint
import json


def random_num():
    start = 10**8
    end = (10**9)-1
    return randint(start, end)

def checkId(id):
    acc = Account.query.filter_by(accountId=id).first()
    if acc is None:
        abort(404)
    return

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

app.register_error_handler(404, page_not_found)
app.register_error_handler(500, internal_server_error)

#  User Login / Logout / Home Routes

# Login route
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
@login_checked
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = request.form.get('username')
        password = request.form.get('password')
        user = UserStore.query.filter_by(username=username).first()
        if user is None:
            flash('Wrong login credentials', 'danger')
        else:
            if sha256_crypt.verify(password, user.password):
                session['is_login'] = True
                session['user'] = username
                flash('Successful Login', 'success')
                return redirect(url_for('home'))
            else:
                flash('Wrong Password', 'danger')
    return render_template('login.html', form=form)


# Logout Route
@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('Successfully Logout', 'success')
    return redirect(url_for('login'))


# Home Route
@app.route('/home')
@login_required
def home():
    return render_template('home.html')


#About Us Route
@app.route("/aboutus")
@login_required
def aboutus():
    return render_template('aboutus.html')


#About Us Route
@app.route("/contactus")
@login_required
def contactus():
    return render_template("contactus.html")


#About Us Route
@app.route("/services")
@login_required
def services():
    return render_template("services.html")


####################################################

#   Customer Management Routes

# City Route
@app.route('/city/<selectState>')
@login_required
def city(selectState):
    states = getstates()
    for i, state in enumerate(states):
        if state == selectState:
            n = i
            break
    cities = getcities()[int(n)]
    cityArray = []
    for city in cities:
        cityObj = {}
        cityObj['id'] = city[0]
        cityObj['name'] = city[1]
        cityArray.append(cityObj)
    return jsonify({'cities': cityArray})

# Customer Route


@app.route('/customer/create', methods=['GET', 'POST'])
@login_required
def customerCreate():
    form = CustomerCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        ssnid = request.form.get('ssnid')
        customerName = request.form.get('customerName')
        age = request.form.get('age')
        state = request.form.get('state')
        city = request.form.get('city')
        if state == None:
            flash('State field Required', 'warning')
        elif city == None:
            flash('City field Required', 'warning')
        else:
            address = city + ", " + state
            if Customer.query.filter_by(ssnid=ssnid).first():
                flash('SSN Id already taken', 'danger')
            else:
                id=0
                while True:
                    id = random_num()
                    if not Customer.query.filter_by(customerId=id).first():
                        break
                newCustomer = Customer(ssnid=ssnid, customerId=id, customerName=customerName, age=age, address=address)
                db.session.add(newCustomer)
                flashMessage = 'Customer creation initiated successfully'
                newStatus = CustomerStatus(ssnid=ssnid, customerId=id, status='active', message=flashMessage, lastUpdated=datetime.now())
                db.session.add(newStatus)
                db.session.commit()
                flash(flashMessage, 'success')
                return redirect(url_for('customerCreate'))
    return render_template('customerCreate.html', form=form)


# Customer Search Route

@app.route('/customer/<status>', methods=['GET', 'POST'])
@login_required
def customerSearch(status):
    form = CustomerSearchForm()
    if status == 'delete':
        redirectTo = 'customerDelete'
    elif status == 'update':
        redirectTo = 'customerUpdate'
    else:
        abort(404)
    if request.method == 'POST' and form.validate_on_submit():
        ssnid = request.form.get('ssnId')
        customerId = request.form.get('customerId')
        if len(ssnid) != 9 and len(customerId) != 9:
            flash('Valid SSN Id / Customer Id Required', 'warning')
        elif len(ssnid) == 9:
            c = Customer.query.filter_by(ssnid=ssnid).first()
            if c:
                print(c.customerId)
                if len(c.customerId) != 9:
                    flash('Deleted! Customer Account not Found', 'danger')
                    return redirect(url_for('customerSearch', status=status))
                return redirect(url_for(redirectTo, id=ssnid))
            else:
                flash('Invalid SSN Id', 'danger')
        else:  
            if Customer.query.filter_by(customerId=customerId).first():
                return redirect(url_for(redirectTo, id=customerId))
            else:
                flash('Invalid Customer Id', 'danger')
    return render_template('customerSearch.html', form=form)


#Update Customer route


@app.route('/customer/<id>/update', methods = ['GET', 'POST'])
@login_required
def customerUpdate(id):
    c = Customer.query.filter_by(ssnid=id).first()
    if c is None:
        c = Customer.query.filter_by(customerId=id).first()
    form  = CustomerUpdateForm()
    states = getstates()
    if request.method == 'POST' and form.validate_on_submit():
        name = request.form.get('customerName')
        age = request.form.get('age')
        state = request.form.get('state')
        city = request.form.get('city')
        if state == None or city == None:
            address = ''
        else:
            address = city + ', ' + state
        try:
            if len(name)>0:
                c.customerName = name
            if len(age)>0:
                c.age = age
            if len(address)>0:
                c.address = address

            flashMessage = 'Customer update initiated successfully'
            newStatus = CustomerStatus(ssnid=c.ssnid, customerId=c.customerId, status='active', message=flashMessage, lastUpdated=datetime.now())
            db.session.add(newStatus)
            db.session.commit()
            flash(flashMessage, 'success')
            return redirect(url_for('home'))
        except Exception as exception:
            flash('Some error message', 'danger')
            
    return render_template('customerUpdate.html', form=form, c=c, states=states)


#Delete Customer Route    


@app.route('/customer/<id>/delete', methods = ['GET', 'POST'])
@login_required
def customerDelete(id):
    c = Customer.query.filter_by(ssnid=id).first()
    if c is None:
        c = Customer.query.filter_by(customerId=id).first()
    if request.method == 'POST':
        flashMessage = 'Customer deletion initiated successfully'
        newStatus = CustomerStatus(ssnid=c.ssnid, customerId=0, status='inactive', message=flashMessage, lastUpdated=datetime.now())
        db.session.add(newStatus)
        acc=Account.query.filter_by(customerId=c.customerId).first()
        if acc is not None:
            flashMessage2 = 'Account deletion initiated successfully'
            newStatus2 = AccountStatus(customerId=c.customerId, accountId=0, accType=acc.AccType, status='inactive', message=flashMessage2, lastUpdated=datetime.now())
            db.session.add(newStatus2)
        Account.query.filter_by(customerId=c.customerId).delete()
        c.customerId = 0
        db.session.commit()
        flash(flashMessage, 'success')
        return redirect(url_for('home'))
    return render_template('customerDelete.html', c=c)



#####################################################

#   Account Management Routes

# Create Account Route
@app.route('/account/create', methods=['GET', 'POST'])
@login_required
def accountCreate():
    form = AccountCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        customerId = request.form.get('customerId')
        accountType = request.form.get('accountType')
        balance = request.form.get('depositAmount')

        if Customer.query.filter_by(customerId=customerId).first():
            if Account.query.filter_by(customerId=customerId, accType=accountType).first():
                flashMessage = 'Customer already has account of specified type'
                a = Account.query.filter_by(customerId=customerId).first()
                newStatus = AccountStatus(customerId=customerId, accountId=a.accountId, accType=accountType, status='active', message=flashMessage, lastUpdated=datetime.now())
                db.session.add(newStatus)
                db.session.commit()
                flash(flashMessage, 'danger')
                return redirect(url_for('accountCreate'))
            else:
                id=0
                while True:
                    id = random_num()
                    if not Account.query.filter_by(accountId=id).first():
                        break
                newAccount = Account(customerId=customerId, accountId=id, accType=accountType, balance=balance)
                db.session.add(newAccount)
                flashMessage = 'Account creation initiated successfully'
                newStatus = AccountStatus(customerId=customerId, accountId=id, accType=accountType, status='active', message=flashMessage, lastUpdated=datetime.now())
                db.session.add(newStatus)
                db.session.commit()
                flash(flashMessage, 'success')
                return redirect(url_for('accountCreate'))
        else:
            flash('Customer Id not found', 'danger')
    return render_template('accountCreate.html', form=form)


# Account Search Route
@app.route('/account/<status>', methods=['GET', 'POST'])
@login_required
def accountSearch(status):
    if status == 'delete':
        redirectTo = 'accountDelete'
    elif status == 'details':
        redirectTo = 'accountDetails'
    else:
        abort(404)
    form = AccountSearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        accountId = request.form.get('accountId')
        customerId = request.form.get('customerId')
        if len(accountId) != 9 and len(customerId) != 9:
            flash('Valid Account Id / Customer Id Required', 'warning')
        elif len(accountId) == 9:
            if Account.query.filter_by(accountId=accountId).first():
                return redirect(url_for(redirectTo, id=accountId))
            else:
                flash('Invalid Account Id', 'danger')
        else:  
            acc=Account.query.filter_by(customerId=customerId).first()
            if acc != None:
                return redirect(url_for(redirectTo, id=acc.accountId))
            else:
                flash('Invalid Customer Id', 'danger')
    return render_template('accountSearch.html', form=form)


# Delete Account Route


@app.route('/account/<id>/delete', methods=['GET', 'POST'])
@login_required
def accountDelete(id):
    c = Account.query.filter_by(accountId=id).first()
    if c is None:
        c = Account.query.filter_by(customerId=id).first()
    if request.method == 'POST':
        flashMessage = 'Account deletion initiated successfully'
        newStatus = AccountStatus(customerId=c.customerId, accountId=0, accType=c.accType, status='inactive', message=flashMessage, lastUpdated=datetime.now())
        Account.query.filter_by(accountId=c.accountId).delete()
        db.session.add(newStatus)
        db.session.commit()
        flash(flashMessage, 'success')
        return redirect(url_for('home'))
    return render_template('accountDelete.html', c=c)

##################################################

#   Status Details Routes

# Customer Status Route
@app.route('/status/customer')
@login_required
def customerStatus():
    customers = CustomerStatus.query.all()
    return render_template('customerStatus.html', customers=customers)


# Account Status Route
@app.route('/status/account')
@login_required
def accountStatus():
    accounts = AccountStatus.query.all()
    return render_template('accountStatus.html', accounts=accounts)


##################################################

#   Transaction Retated routes

# Account Details Route
@app.route('/account/<id>/details')
@login_required
def accountDetails(id):
    checkId(id)
    acc = Account.query.filter_by(accountId=id).first()
    return render_template('accountDetails.html', acc=acc, id=id)


# Deposit Amount Route 
@app.route('/account/<id>/deposit', methods=['GET', 'POST'])
@login_required
def amountDeposit(id):
    checkId(id)
    form = DepositAmountForm()
    acc = Account.query.filter_by(accountId=id).first()
    if request.method == 'POST' and form.validate_on_submit():
        amount = request.form.get('amount')
        acc.balance = int(acc.balance) + int(amount)
        
        transactionId = 0
        while True:
            transactionId = random_num()
            if not TransactionStatement.query.filter_by(transactionId=transactionId).first():
                        break
        newTransaction = TransactionStatement(accountId=id, transactionId=transactionId, description='Deposit', date=datetime.now(), amount=int(amount), balance=acc.balance)
        db.session.add(newTransaction)

        db.session.commit()
        flash('Amount deposited successfully', 'success')
        return redirect(url_for('accountDetails', id=id))
    return render_template('amountDeposit.html', form=form, acc=acc, id=id)


# WithDraw Amount Route
@app.route('/account/<id>/withdraw', methods=['GET', 'POST'])
@login_required
def amountWithdraw(id):
    checkId(id)
    form = WithDrawAmountForm()
    acc = Account.query.filter_by(accountId=id).first()
    if request.method == 'POST' and form.validate_on_submit():
        amount = request.form.get('amount')
        print(type(acc.balance))
        if int(acc.balance) > int(amount):
            acc.balance = int(acc.balance) - int(amount)

            transactionId = 0
            while True:
                transactionId = random_num()
                if not TransactionStatement.query.filter_by(transactionId=transactionId).first():
                            break
            newTransaction = TransactionStatement(accountId=id, transactionId=transactionId, description='Withdraw', date=datetime.now(), amount=int(amount), balance=acc.balance)
            db.session.add(newTransaction)

            db.session.commit()
            flash('Amount withdrawn successfully', 'success')
            return redirect(url_for('accountDetails', id=id))
        else:
            flash('Withdraw not allowed, please choose smaller amount', 'danger')
    return render_template('amountWithdraw.html', form=form, acc=acc, id=id)


# Transfer Money Route
@app.route('/account/<id>/transfer', methods=['GET', 'POST'])
@login_required
def amountTransfer(id):
    checkId(id)
    form = TransferAmountForm()
    if request.method == 'POST' and form.validate_on_submit():
        sourceId = request.form.get('sourceAccId')
        targetId = request.form.get('targetAccId')
        amount = request.form.get('amount')
        sourceAcc = Account.query.filter_by(accountId=sourceId).first()
        targetAcc = Account.query.filter_by(accountId=targetId).first()
        if targetAcc is not None:
            if int(sourceAcc.balance) > int(amount):
                sourceAcc.balance = int(sourceAcc.balance) - int(amount)
                targetAcc.balance = int(targetAcc.balance) + int(amount)

                transactionId = 0
                while True:
                    transactionId = random_num()
                    if not TransactionStatement.query.filter_by(transactionId=transactionId).first():
                        break

                sourceTransaction = TransactionStatement(accountId=sourceId, transactionId=transactionId, description='Transfer', date=datetime.now(), amount=int(amount), balance=sourceAcc.balance)
                targetTransaction = TransactionStatement(accountId=targetId, transactionId=transactionId, description='Transfer', date=datetime.now(), amount=int(amount), balance=targetAcc.balance)
                db.session.add(sourceTransaction)
                db.session.add(targetTransaction)

                db.session.commit()
                flash('Amount transfer completed successfully', 'success')
                return redirect(url_for('accountDetails', id=id))
            else:
                flash('Transfer not allowed, please choose smaller amount', 'warning')
        else:
            flash('Wrong Target Account ID', 'danger')
    return render_template('amountTransfer.html', form=form, accountId=id, id=id)


# Account Statement Route
@app.route('/account/<id>/statement', methods=['GET', 'POST'])
@login_required
def accountStatement(id):
    checkId(id)
    if request.method == 'POST':
        radio = request.form.get('radiobtn')
        if radio == 'radiobtn1':
            ntrans = request.form.get('noOfTransaction')
            datas = TransactionStatement.query.filter_by(accountId=id).limit(int(ntrans)).all()
            return render_template('accountStatement.html', datas=datas, id=id)
        elif radio == 'radiobtn2':
            sdate = request.form.get('startDate') + ' 00:00:00'
            edate = request.form.get('endDate') + ' 23:59:59'
            datas = TransactionStatement.query.filter_by(accountId=id).filter(TransactionStatement.date.between(sdate,edate)).all()
            return render_template('accountStatement.html', datas=datas, id=id)
        else:
            flash('All Field Required', 'danger')
    return render_template('accountStatement.html', id=id)


###################################################


