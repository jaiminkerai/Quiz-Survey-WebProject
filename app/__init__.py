'''
Tells python that the app directory is a package.
Initialises and congregates the app. 
'''

from flask import Flask
from config import Config, TestConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler
from logging.handlers import RotatingFileHandler
import os
from flask_mail import Mail
from flask_moment import Moment

app = Flask(__name__) # Instantiate Flask application; __name__ a variable equal to the name of the module
app.config.from_object(Config)
db = SQLAlchemy(app) # Create a database instance
migrate = Migrate(app, db)
app.config['FLASK_ADMIN_SWATCH'] = 'cosmo'

moment = Moment(app) # Instantiating flask moments

login = LoginManager(app)
login.login_view = 'login' # Tells @login_required the route for the login
login.login_message_category = "alertInfo" #Category for need to login before accessing page messages on base.html

mail = Mail(app)

from app import routes, models, errors

if not app.debug: #When debug mode is FALSE
    # Log errors to an email
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Quizards Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

        # Log errors to a file
        if not os.path.exists('logs'):
            os.mkdir('logs')
        # When an error occurs, a directory called logs will appear. The error will be stored in a newly created project2.log
        file_handler = RotatingFileHandler('logs/errors.log', maxBytes=10240, backupCount=10) 
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Quizards startup')