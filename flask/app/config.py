import os

base = os.path.dirname(os.path.abspath(__file__))

def load_email(email):
    path = os.path.join(base, 'emails', email)
    with open(path, 'r') as f:
        return f.read()

def get_database_uri():
    db_protocol = os.environ.get('DB_PROTOCOL', 'mysql')
    db_username = os.environ.get('DB_USERNAME', 'flask')
    db_password = os.environ.get('DB_PASSWORD')
    db_domain = os.environ.get('DB_DOMAIN', 'db')
    db_database = os.environ.get('DB_DATABASE', 'shadowmail')
    return f'{db_protocol}://{db_username}:{db_password}' \
           f'@{db_domain}/{db_database}'

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
    CREATE_EMAIL_RATE_LIMIT = '3/30minutes'
    REQUEST_DELETE_RATE_LIMIT = '1/30minutes'

class Testing(Config):
    CSRF_ENABLED = False
    SECRET_KEY = 'change_me'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
    BEAUTIFURL_DICTIONARIES_URI = os.path.join(base, 'test_dictionaries')
    BEAUTIFURL_FORMAT = 'w'

class Development(Config):
    TESTING = False
    SECRET_KEY = 'change_me'
    SQLALCHEMY_DATABASE_URI = get_database_uri()
    IP_RATE_LIMIT = '1000/30minutes'
    CREATE_EMAIL_RATE_LIMIT = '3000/30minutes'
    REQUEST_DELETE_RATE_LIMIT = '1000/30minutes'

class Docker(Config):
    DEVELOPMENT = False
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = get_database_uri()
    MAIL_SERVER = 'postfix'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
