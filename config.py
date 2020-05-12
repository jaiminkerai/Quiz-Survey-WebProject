import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Admin Email Configuration to receive emails (in event of errors...)
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = 1
    MAIL_USERNAME = 'cits3403test@gmail.com'
    MAIL_PASSWORD = '3403projecttest'
    ADMINS = ['22718975@student.uwa.edu.au']

    #Posts per page configuration
    POSTS_PER_PAGE = 25
