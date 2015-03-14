from app.app_and_db import db
from datetime import datetime

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    confirmed_at = db.Column(db.DateTime())
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
    email = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    first_name = db.Column(db.String(50), nullable=False, server_default='')

    # Relationships
    storms = db.relationship('ThunderStorm', backref='storms', lazy='dynamic')
    blasts = db.relationship('Blast', secondary='user_blasts', backref=db.backref('users', lazy='dynamic'))
    
    # https://flask-login.readthedocs.org/en/latest/#your-user-class
    def is_active(self):
        return True

    def get_id(self):
        return unicode(self.id)

    def is_authenticated(self):
        # activated their account
        return self.active
    
    def is_anonymous(self):
        # Returns True if this is an anonymous user
        
        return False


class Blast(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    creation = db.Column(db.DateTime, nullable=False, default=datetime.today())
    status = db.Column(db.String(), nullable=False, default="Pending")
    creater = db.Column(db.Integer, db.ForeignKey('user.id'))


class UserBlasts(db.Model):

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    blast_id = db.Column(db.Integer(), db.ForeignKey('blast.id', ondelete='CASCADE'))
    

class ThunderStorm(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    creation = db.Column(db.DateTime, nullable=False, default=datetime.today())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.String(), nullable=False, default="Pending")


