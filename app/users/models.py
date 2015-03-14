from app.app_and_db import db
from datetime import datetime

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    confirmed_at = db.Column(db.DateTime())
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
    first_name = db.Column(db.String(50), nullable=False, server_default='')
    last_name = db.Column(db.String(50), nullable=False, server_default='')

    # Relationships
    user_auth = db.relationship('UserAuth', uselist=False)
    storms = db.relationship('ThunderStorm', backref='storms', lazy='dynamic')
    blasts = db.relationship('Blast', secondary='user_blasts', backref=db.backref('users', lazy='dynamic'))
    



class UserAuth(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    reset_password_token = db.Column(db.String(100), nullable=False, server_default='')
    active = db.Column(db.Boolean(), nullable=False, server_default='0')

    user = db.relationship('User', uselist=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))


class Role(db.Model):

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(255))


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


