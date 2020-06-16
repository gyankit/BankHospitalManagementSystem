from functools import wraps
from flask import session, request, redirect, url_for, flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'is_login' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first', 'warning')
            return redirect(url_for('login', next=request.url))
    return decorated_function

def login_checked(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'is_login' in session:
            flash('Already Login', 'warning')
            return redirect(url_for('home'))
        else:
            return f(*args, **kwargs)
    return decorated_function