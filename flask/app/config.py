import os

def load_email(email):
    with open('emails/' + email, 'r') as f:
        return f.read()

class Config:
    DEBUG = True
    TESTING = True
    DEVELOPMENT = True
    CSRF_ENABLED = True
    SECRET_KEY = ''
    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    EMAIL_POSTFIX = '@shadowmail.co.uk'
    BEAUTIFURL_DICTIONARIES_URI = None
    BEAUTIFURL_FORMAT = 'aaA'

    DELETE_TOKEN_EXPIRY = 60 * 30

    MAIL_SENDER = 'no-reply@shadowmail.co.uk'
    MAIL_DELETE_REQUEST_SUBJECT = 'Shadowmail Delete Request'
    MAIL_DELETE_REQUEST_BODY = load_email('request_delete')

    IP_RATE_LIMIT = '10/30minutes'

class Development(Config):
    CSRF_ENABLED = False
    SECRET_KEY = 'change_me'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
    BEAUTIFURL_DICTIONARIES_URI = 'test_dictionaries'
    BEAUTIFURL_FORMAT = 'w'

class Docker(Config):
    DEVELOPMENT = False
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = 'mysql://flask:' + os.environ['DB_PASSWORD'] + '@db/shadowmail'
