from flask import Flask, redirect, render_template, render_template_string, flash
from flask import request, url_for
from app.app_and_db import app, db
from app.users.forms import UserProfileForm, LoginForm, RegisterForm
from app.users.models import User, authenticate
from app.tc.models import Blast, ThunderStorm
from flask_mail import Message
from flask_login import login_required, login_user, logout_user, current_user

login_manager = app.extensions.get('login_manager', None)
#login_manager.login_view = "users.login"

@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))



@app.route('/blast', methods=['POST'])
@login_required
def user_blast_page():

    blast = Blast()
    blast.creater = current_user.id
    #user=User.query.join(UserAuth).filter_by(username=request.form['blast_user']).first()
    user = User.query.filter_by(username=request.form['blast_user']).first()
    user.blasts.append(blast)
    
    # this needs to be done after blast is no longer pending
    # if len(user.blasts) == 5:
    #     ts = ThunderStorm()
    #     user.storms.append(ts)
    # notify everyone.

    db.session.add(user)
    db.session.commit()

    # Notify user.
    if not app.debug:
        message = Message("Blast", 
            recipients=user.email,
            html = "You have been blased by "+ current_user.first_name,
            body = "You have been blased by "+ current_user.first_name)

        mail_engine = app.extensions.get('mail', None)
        mail_engine.send(msg)



    if user.id == current_user.id:
        return "you blasted yourself"
    
    return redirect(url_for('home_page'))
