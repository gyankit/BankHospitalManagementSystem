from App import app, db
from flask import render_template, redirect, request, url_for, flash, session
from passlib.hash import sha256_crypt
from App.forms import LoginForm
import json


@app.route('/')
@app.route('/index')
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        return redirect(url_for('home'))
    return render_template('login.html', form=form)


@app.route('/home')
def home():
    return render_template('home.html')
