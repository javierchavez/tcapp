from flask_wtf import Form
from wtforms import StringField, SubmitField, validators, StringField, PasswordField



class RegisterForm(Form):

    first_name = StringField('First name',
                             validators=[validators.DataRequired('First name is required')])
    username = StringField('Username',
                            validators=[validators.DataRequired('Last name is required')])
    email = StringField('Email',
                            validators=[validators.DataRequired('Last name is required')])
    password = PasswordField('Password',
                             validators=[validators.DataRequired('Password is required')])
    submit = SubmitField('Submit')


class LoginForm(Form):
    
    username = StringField('Username',
                      validators=[validators.DataRequired('First name is required')])
    password = PasswordField('Password',
                             validators=[validators.DataRequired('Password is required')])

# Define the User profile form
class UserProfileForm(Form):
    first_name = StringField('First name',
                             validators=[validators.DataRequired('First name is required')])
    last_name = StringField('Last name',
                            validators=[validators.DataRequired('Last name is required')])
    submit = SubmitField('Save')
