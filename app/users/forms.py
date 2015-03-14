from flask_wtf import Form
from wtforms import StringField, SubmitField, validators, StringField, PasswordField



class MyRegisterForm(Form):

    first_name = StringField('First name',
                             validators=[validators.DataRequired('First name is required')])
    last_name = StringField('Last name',
                            validators=[validators.DataRequired('Last name is required')])

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
