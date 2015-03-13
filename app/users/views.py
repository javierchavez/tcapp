from flask import Flask, redirect, render_template, render_template_string
from flask import request, url_for
from flask_user import current_user, login_required
from app.app_and_db import app, db
from app.users.forms import UserProfileForm
from app.users.models import User, UserAuth, Blast, ThunderStorm
from flask_mail import Message

@app.route('/user/profile', methods=['GET', 'POST'])
@login_required
def user_profile_page():
    
    form = UserProfileForm(request.form, current_user)
    if request.method=='POST' and form.validate():
        
        form.populate_obj(current_user)
        db.session.commit()
        return redirect(url_for('home_page'))

    return render_template('users/user_profile_page.html',
        form=form)

@app.route('/u/<uname>', methods=['GET'])
def user_public_profile_page(uname=None):

    user=User.query.join(UserAuth).filter_by(username=uname).first()

    if user is None:
        return "Nonthing here"

    return render_template('users/user_public_profile_page.html', user=user)

@app.route('/blast', methods=['POST'])
@login_required
def user_blast_page():

    blast = Blast()
    blast.creater = current_user.id
    user=User.query.join(UserAuth).filter_by(username=request.form['blast_user']).first()
    user.blasts.append(blast)
    
    # this needs to be done after blast is no longer pending
    # if len(user.blasts) == 5:
    #     ts = ThunderStorm()
    #     user.storms.append(ts)

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

@app.route('/stats', methods=['GET'])
def user_stats_page():

    users = User.query.all()
    return render_template('pages/stats_page.html', users=users)



