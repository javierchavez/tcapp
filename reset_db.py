from __future__ import print_function
import datetime
from app.app_and_db import app, db
from app.startup.init_app import init_app
from app.users.models import  User
from app.tc.models import Blast, UserBlasts, ThunderStorm
from passlib.hash import pbkdf2_sha256

def reset_db(app, db):

    
    print('Dropping all tables')
    db.drop_all()

    # Create all tables
    print('Creating all tables')

    db.create_all()
    # Add users
    print('Adding users')
    add_user(app, db, 'bobby', 'Bob', 'User', 'admin@example.com', 'Password1')
    add_user(app, db, 'jony', 'John', 'User', 'admin2@example.com', 'Password1')
    # user.roles.append(admin_role)
    db.session.commit()

def add_user(app, db, username, first_name, last_name, email, password):
    """
    Create UserAuth and User records.
    """
    password = pbkdf2_sha256.encrypt(password, rounds=10, salt_size=16) 
    user = User(
        active=True,
        first_name=first_name,
        username=username,
        email=email,
        hashed_password=password,
        confirmed_at=datetime.datetime.now(),
        
    )
    
    db.session.add(user)
    return user


# Initialize the app and reset the database
if __name__ == "__main__":
    init_app(app, db)
    reset_db(app, db)
