from flask import Flask, redirect, render_template, render_template_string
from flask import request, url_for
from app.app_and_db import app, db
from app.users.forms import UserProfileForm, LoginForm, RegisterForm
from app.users.models import User, Blast, ThunderStorm
from flask_mail import Message
from flask_login import login_required, login_user, logout_user, current_user

login_manager = app.extensions.get('login_manager', None)



@login_manager.user_loader
def load_user(userid):
    return User.get(int(userid))


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # login and validate the user...
        is_vaild = User.authenticate(response.form['username'], response.form['password'])
        if (is_vaild):
            login_user(user)
            flash("Logged in successfully.")
            return redirect(request.args.get("next") or url_for("index"))
        else:
            flash("Error.")

    return render_template("users/user_login_page.html", form=form)

@app.route('/register', methods=['GET', 'POST'])
def user_register_page():
    form = RegisterForm(request.form)
    
    if request.method=='POST' and form.validate():
        user = User()
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        # send email confirmation 
        return redirect(url_for('home_page'))
    
    return render_template('users/user_register_page.html', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home_page'))


@app.route('/user/profile', methods=['GET', 'POST'])

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

# TODO
# for user authentication and 
# for password reset i will use
# https://pythonhosted.org/itsdangerous/
# auth: Signer
# pwdrst: Timestamp



@app.route('/blast', methods=['POST'])
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

@app.route('/notifications', methods=['GET'])
def user_notif_page():
    # there has gotta be a better way?!
    pend = Blast.query.filter_by(status="Pending").join(User).filter_by(email=current_user.email).values(Blast.id, Blast.creation, Blast.status, User.first_name)
    other = Blast.query.filter(~Blast.status.contains("Pending")).join(User).filter_by(email=current_user.email)

    resultlist = []
    for id, creation, status, creater in pend:
        resultlist.append({'creation': creation,
                           'status': status,
                           'creater': creater})

    return render_template('pages/user_notifications_page.html', pending=resultlist, other=other)




