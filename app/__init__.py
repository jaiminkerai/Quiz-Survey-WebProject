from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler
from logging.handlers import RotatingFileHandler
import os
from flask_mail import Mail
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
mail = Mail(app)
admin = Admin(app)

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
        app.logger.info('Quizzards startup')

admin.add_view(ModelView(models.User, db.session))
admin.add_view(ModelView(models.Quizzes, db.session))
admin.add_view(ModelView(models.Questions, db.session))
