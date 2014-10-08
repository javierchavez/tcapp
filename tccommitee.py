from datetime import datetime
from flask import Flask, request, render_template_string, render_template


from sqlalchemy.orm import sessionmaker
# Use a Class-based config to avoid needing a 2nd file
from flask.ext.babel import Babel
from flask.ext.login import current_user
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.user import current_user, login_required, UserManager, UserMixin, SQLAlchemyAdapter


class ConfigClass(object):
    # Configure Flask
    SECRET_KEY = 'THIS IS AN INSECURE SECRET'                 # Change this for production!!!
    SQLALCHEMY_DATABASE_URI = 'sqlite:///minimal_app.sqlite'  # Use Sqlite file db
    CSRF_ENABLED = True
    USER_ENABLE_EMAIL = False

app = Flask(__name__)
app.config.from_object(__name__+'.ConfigClass')



# Initialize Flask extensions
babel = Babel(app)                              # Initialize Flask-Babel
db = SQLAlchemy(app)                            # Initialize Flask-SQLAlchemy

Session = sessionmaker()

@babel.localeselector
def get_locale():
    translations = [str(translation) for translation in babel.list_translations()]
    return request.accept_languages.best_match(translations)

# join table
blasts = db.Table('blasts',
                  db.Column('blast_id', db.Integer, db.ForeignKey('blast.id')),
                  db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

# Define User model. UserMixin
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean(), nullable=False, default=False)
    status = db.Column(db.Boolean(), nullable=False, default=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, default='')
    thunderstorms = db.relationship('ThunderStorm', backref='user', lazy='dynamic')
    blasts = db.relationship('Blast', secondary=blasts,
                             backref=db.backref('users', lazy='dynamic'))


# Define Blast model
class Blast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creation = db.Column(db.DateTime, nullable=False, default=datetime.today())
    status = db.Column(db.String(), nullable=False, default="Pending")
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))


# Define TS model.
class ThunderStorm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creation = db.Column(db.DateTime, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))




# Create all database tables
db.create_all()

# Setup Flask-User
db_adapter = SQLAlchemyAdapter(db,  User)       # Select database adapter
user_manager = UserManager(db_adapter, app)     # Init Flask-User and bind to app


@app.route('/test')
def hello_world():
    if current_user.is_authenticated():
        return profile_page()
    return render_template_string("""
            {% extends "base.html" %}
            {% block content %}
            <h2>{%trans%}Home Page{%endtrans%}</h2>
            <p> <a href="{{ url_for('user.login') }}">{%trans%}Sign in{%endtrans%}</a> or
                <a href="{{ url_for('user.register') }}">{%trans%}Register{%endtrans%}</a></p>
            {% endblock %}
            """)


# The '/profile' page requires a logged-in user
@app.route('/profile')
@login_required                                 # Use of @login_required decorator
def profile_page():
    return render_template_string("""
        {% extends "base.html" %}
        {% block content %}
            <h2>{%trans%}Profile Page{%endtrans%}</h2>
            <p> {%trans%}Hello{%endtrans%}
                {{ current_user.username or current_user.email }},</p>
            <p> <a href="{{ url_for('user.change_username') }}">
                {%trans%}Change username{%endtrans%}</a></p>
            <p> <a href="{{ url_for('user.change_password') }}">
                {%trans%}Change password{%endtrans%}</a></p>
            <p> <a href="{{ url_for('user.logout') }}?next={{ url_for('user.login') }}">
                {%trans%}Sign out{%endtrans%}</a></p>
        {% endblock %}
        """)


# The '/profile' page requires a logged-in user
@app.route('/stats')
@login_required
def stats_page():
    # return only users with blasts
    # users = User.query.join(User.blasts, aliased=True).filter_by(status=True)
    # print(users)

    # only display blasts that are approved
    # [user for u in user.blasts ]
    users = [user for user in User.query.all()]

    return render_template('stats.html', users=User.query.all())



@app.route('/rules')
@login_required
def rules_page():



    return render_template('rules.html')


@app.route('/blast', methods=['GET', 'POST'])
@login_required
def new_blast():
    # get all the users not include yourself
    users = [instance for instance in User.query.filter(User.username.isnot(current_user.username))]
    if request.method == 'POST':

        kv_user = dict(request.form)
        # this is a "hack"
        blasted_user = User.query.filter_by(username=kv_user['user'][0]).first()
        # create a blast add user that blast belongs to
        bl = Blast(user_id=current_user.id)
        # add blast to DB
        db.session.add(bl)
        blasted_user.blasts.append(bl)
        # associate the current user to the blast

        # current_user.blasts.append(bl)

        db.session.commit()
        return render_template('blast.html', users=users)

    else:
        return render_template('blast.html', users=users)

class TcCard(object):
    def __init__(self):
        self.blaster = ''
        self.blastee = ''
        self.datetime = ''
        self.status = ''

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    # this is the main screen of the app
    # LOGIN req
    # news feed (all updats in DB)
    napp = [bl for bl in current_user.blasts if bl.status == "Pending"]
    my_disputed_blasts = [bl for bl in Blast.query.filter_by(status="Dispute").filter_by(user_id=current_user.id)]
    print(my_disputed_blasts)
    # cards = [ for data in User.query.all()]
    if request.method == 'POST':
        print(request.form)
        kv_a = dict(request.form)
        resp = kv_a['answer'][0]
        print(resp)
        if resp == 'a':
            pass
        elif resp == 'd':
            pass
        else:
            return render_template('index.html')


    blstr = ''
    if len(napp) > 0:
        bltr = napp[0].user_id
        blstr = User.query.get(bltr).username


    return render_template('index.html', needs_app=napp, blaster=blstr, my_disputes=my_disputed_blasts)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
