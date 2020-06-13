from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or 'TCSGroupCaseStudy'

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@server/db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/casestudy1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from App import routes