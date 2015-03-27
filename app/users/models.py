from app.app_and_db import db, app
from datetime import datetime
from passlib.hash import pbkdf2_sha256
from pytz import timezone
from app.tc.models import Blast

def get_dt():
    '''Return the time at given timezone in utc'''
    # Current time in UTC
    now_utc = datetime.now(timezone('UTC'))
    return  now_utc.astimezone(timezone('US/Mountain')).strftime("%Y-%m-%d %H:%M:%S %Z%z")

class Object:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    confirmed_at = db.Column(db.DateTime)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
    first_name = db.Column(db.String(50), nullable=False, server_default='')
    username = db.Column(db.String(50), nullable=False, unique=True)
    hashed_password = db.Column(db.String)
    
    # Relationships
    # user has many messages
    # user has many storms
    storms = db.relationship('ThunderStorm', backref='storms', lazy='dynamic')
    # user has many blasts
    blasts = db.relationship('Blast',
                             secondary='user_blasts',
                             backref=db.backref('users', lazy='dynamic'),
                             order_by='Blast.creation')
    conversations = db.relationship('Conversation',
                                    secondary='user_conversations',
                                    backref=db.backref('users', lazy='dynamic'))
    
    # https://flask-login.readthedocs.org/en/latest/#your-user-class
    def is_active(self):
        # a more specific type of registered user. all reg. users will be active.
        return True

    def get_id(self):
        return unicode(self.id)

    def is_authenticated(self):
        # activated their account via email 
        # dont want to worry about email when testing
        if app.debug: return True
        return self.active
    
    def is_anonymous(self):
        # Returns True if this is an anonymous user
        return not self.active

    def get_notifications(self):
        return  map(lambda u: Object(creater=User.query.get(u.creater).username, rest=u), self.blasts)

    def get_blast(self, b_id):
        to_check = Blast.query.get(b_id)
        #if self.blasts
        return to_check 
    
    def get_pending(self):
        # map reduce
        mapped = map(lambda u: Object(creater=User.query.get(u.creater).username, rest=u), self.blasts)
        return filter(lambda x: x.rest.status == "Pending", mapped)

    def get_pending_len(self):
        return len(filter(lambda x: x.status == "Pending", self.blasts))
    
    # before save hash password..
    # The key needs to be different than what attribute you are changing. More specifically,
    # wtf forms gets all the attributes supplied in the form, it then recursivly sets attributes
    # while they dont match. so If we supply a password field and hash it and save it then wtf
    # forms is going to see its different call __setattr__ again and a infinite loops continues,
    #because we are setting a hash and wtf it trying to set it. so I just look when wtf forms
    # tries to set a field called password and set some other field I didnt supply.
    def __setattr__(self, key, value):
        super(User, self).__setattr__(key, value)
        if key == 'password':
            #pwd = self.password
            hashz = pbkdf2_sha256.encrypt(value, rounds=10, salt_size=16)
            self.hashed_password = hashz

# user auth
def authenticate(usern, pwd):
    user = User.query.filter_by(username=usern).first()
    if user is not None:
        return user if _varify_password(pwd, user.hashed_password) else None
    else:
        return None

def _varify_password(given, current):
    return pbkdf2_sha256.verify(given, current)

