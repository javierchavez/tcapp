from flask_wtf import Form
from wtforms import StringField, SubmitField, validators, StringField, PasswordField


# Define the User registration form
# It augments the Flask-User RegisterForm with additional fields
class MyRegisterForm(Form):

    first_name = StringField('First name',
                             validators=[validators.DataRequired('First name is required')])
    last_name = StringField('Last name',
                            validators=[validators.DataRequired('Last name is required')])

class LoginForm(Form):
    
    email = StringField('email',
                      validators=[validators.DataRequired('First name is required')])
    password = PasswordField('password',
                             validators=[validators.DataRequired('Password is required')])

# Define the User profile form
class UserProfileForm(Form):
    first_name = StringField('First name',
                             validators=[validators.DataRequired('First name is required')])
    last_name = StringField('Last name',
                            validators=[validators.DataRequired('Last name is required')])
    submit = SubmitField('Save')
