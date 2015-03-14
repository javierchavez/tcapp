from app.app_and_db import db
from datetime import datetime
from passlib.hash import pbkdf2_sha256

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    confirmed_at = db.Column(db.DateTime())
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
    #password = db.Column(db.String)
    first_name = db.Column(db.String(50), nullable=False, server_default='')
    username = db.Column(db.String(50), nullable=False, unique=True)
    hashed_password = db.Column(db.String)
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

    def authenticate(self, usern, pwd):
        user = User.query.filter_by(username=usern).first()
        if user is not None:
            return pbkdf2_sha256.verify(pwd, user.password)
        else:
            return False

    # before save hash password..
    # The key needs to be different due to wtf forms. It tries to populate obj
    # over and over due to the change in its value after this function finished 
    # causing infinite an loop. so when the attr password tries to be set i set
    # soething else and ignore. 
    def __setattr__(self, key, value):
        super(User, self).__setattr__(key, value)
        if key == 'password':
            #pwd = self.password
            hashz = pbkdf2_sha256.encrypt(value, rounds=10, salt_size=16)
            self.hashed_password = hashz

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


