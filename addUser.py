from App import db
from App.models import UserStore
from passlib.hash import sha256_crypt
from datetime import datetime

user = UserStore('admin', sha256_crypt.hash('admin'), datetime.now)
db.session.add(user)
db.session.commit()