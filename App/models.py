from App import app, db
from datetime import datetime


class UserStore(db.Model):
    __tablename__ = 'userstore'
    id = db.Column( db.Integer, primary_key=True )
    username = db.Column( db.String(80), unique=True, nullable=False )
    password = db.Column( db.String(256), nullable=False )
    datetime = db.Column( db.DateTime(timezone=True), nullable=False, default=datetime.utcnow )

    def __init__(self, username, password, datetime):  
        self.username = username
        self.password = password
        self.datetime = datetime

    def __repr__(self):
        return '<User %r' % self.username


class Customer(db.Model):
    __tablename__ = 'customers'
    ssnid = db.Column(db.String(9), primary_key=True)
    customerId = db.Column(db.String(9), nullable=False, default=0)
    customerName = db.Column(db.String(80), nullable=False)
    age = db.Column(db.String(3), nullable=False)
    address = db.Column(db.String(100), nullable=False)

    def __init__(self, ssnid, customerId, customerName, age, address):
        self.ssnid = ssnid
        self.customerId = customerId
        self.customerName = customerName
        self.age = age
        self.address = address

    def __repr__(self):
        return '<Customer %r' % self.ssnid


class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer ,primary_key=True)
    customerId = db.Column(db.String(9), nullable=False)
    accountId = db.Column(db.String(9), nullable=False, default=0)
    accType = db.Column(db.String(20), nullable=False)
    balance = db.Column(db.Integer, nullable=False)

    def __init__(self, customerId, accountId, accType, balance):
      self.customerId = customerId
      self.accountId = accountId
      self.accType = accType
      self.balance = balance

    def __repr__(self):
        return '<Account %r' % self.customerId

class CustomerStatus(db.Model):
    __tablename__ = 'customerstatus'
    id = db.Column(db.Integer ,primary_key=True)
    ssnid = db.Column(db.String(9), nullable=False)
    customerId = db.Column(db.String(9), nullable=False)
    status = db.Column(db.String(20))
    message = db.Column(db.String(100))
    lastUpdated = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)

    def __init__(self, ssnid, customerId, status, message, lastUpdated):
        self.ssnid=ssnid
        self.customerId=customerId
        self.status=status
        self.message=message
        self.lastUpdated=lastUpdated

    def __repr__(self):
        return '<CustomerStatus %r' % self.ssnid


class AccountStatus(db.Model):
    __tablename__ = 'accountstatus'
    id = db.Column(db.Integer ,primary_key=True)
    customerId = db.Column(db.String(9), nullable=False)
    accountId = db.Column(db.String(9), nullable=False, default=0)
    accType = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20))
    message = db.Column(db.String(100))
    lastUpdated = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)

    def __init__(self, customerId, accountId, accType, status, message, lastUpdated):
        self.customerId=customerId
        self.accountId=accountId
        self.accType=accType
        self.status=status
        self.message=message
        self.lastUpdated=lastUpdated


    def __repr__(self):
        return '<AccountStatus %r' % self.customerId


class TransactionStatement(db.Model):
    __tablename__ = 'transcationstatement'
    id = db.Column(db.Integer ,primary_key=True)
    accountId = db.Column(db.String(9), nullable=False)
    transactionId = db.Column(db.String(9), nullable=False)
    description = db.Column(db.String(10), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    amount = db.Column(db.Integer, nullable=False)
    balance = db.Column(db.Integer, nullable=False)

    def __init__(self, accountId, transactionId, description, date, amount, balance):
        self.accountId=accountId
        self.transactionId=transactionId
        self.description=description
        self.date=date
        self.amount=amount
        self.balance=balance

    def __repr__(self):
        return '<Transaction id %r' % self.transactionId
