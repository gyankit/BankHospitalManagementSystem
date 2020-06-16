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
