import logging
from logging.handlers import SMTPHandler
from flask_mail import Mail
from flask_login import LoginManager
# from flask_user import UserManager, SQLAlchemyAdapter


def init_app(app, db, extra_config_settings={}):
    """
    Initialize Flask applicaton
    """

    # Initialize app config settings
    app.config.from_object('app.startup.settings')
    app.config.update(extra_config_settings)      
    if app.testing:
        app.config['WTF_CSRF_ENABLED'] = False    

    # Setup Flask-Mail
    mail = Mail(app)

    # Doing this due to login not being avail in exentions.
    # https://github.com/mitsuhiko/flask/blob/6e6a3e8cfb5c8c6b6bcddeb0a045a8441a35ad0a/flask/app.py#L477
    login_manager = LoginManager()
    login_manager.init_app(app)
    app.extensions['login_manager'] = login_manager
    
    # Setup an error-logger to send emails to app.config.ADMINS
    # init_error_logger_with_email_handler(app)
    
    from app.users.models import User, Blast, UserBlasts, ThunderStorm
    
    from app.users.forms import RegisterForm, LoginForm
    from app.users.views import user_profile_page

    
    # db_adapter = SQLAlchemyAdapter(db, User,        # Setup the SQLAlchemy DB Adapter
            # UserAuthClass=UserAuth)                 #   using separated UserAuth/User data models
    # user_manager = UserManager(db_adapter, app,     # Init Flask-User and bind to app
    #         register_form=MyRegisterForm,           #   using a custom register form with UserProfile fields
    #         user_profile_view_function = user_profile_page,
    #         )

    from app.users import models
    from app.pages import views
    from app.users import views
    # from 
    return app


def init_error_logger_with_email_handler(app):
    """
    Initialize a logger to send emails on error-level messages.
    Unhandled exceptions will now send an email message to app.config.ADMINS.
    """
    if app.debug: return                        # Do not send error emails while developing

    # Retrieve email settings from app.config
    host      = app.config['MAIL_SERVER']
    port      = app.config['MAIL_PORT']
    from_addr = app.config['MAIL_DEFAULT_SENDER']
    username  = app.config['MAIL_USERNAME']
    password  = app.config['MAIL_PASSWORD']
    secure = () if app.config.get('MAIL_USE_TLS') else None

    # Retrieve app settings from app.config
    to_addr_list = app.config['ADMINS']
    subject = app.config.get('APP_SYSTEM_ERROR_SUBJECT_LINE', 'System Error')

    # Setup an SMTP mail handler for error-level messages
    mail_handler = SMTPHandler(
        mailhost=(host, port),                  # Mail host and port
        fromaddr=from_addr,                     # From address
        toaddrs=to_addr_list,                   # To address
        subject=subject,                        # Subject line
        credentials=(username, password),       # Credentials
        secure=secure,
    )
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

    # Log errors using: app.logger.error('Some error message')
