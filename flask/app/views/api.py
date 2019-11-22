import hashlib
import re
import time

from flask_api import status
from flask_mail import Message
from flask_limiter.util import get_remote_address

from beautifurl import Beautifurl
import limits
from sqlalchemy.exc import InvalidRequestError, IntegrityError
from flask import request

from main import app, db, email_limiter, ip_limiter, mail
from models.virtual_alias import VirtualAlias


EMAIL_REGEX = '.+@.+'

@email_limiter.request_filter
def no_email_whitelist():
    data = request.get_json()
    return data is None or 'email' not in data

def get_email_from_request():
    data = request.get_json(force=True)
    return data['email']

IP_ERROR_MESSAGE = 'Exceeded limit from same ip address: {}'.format(
    limits.parse(app.config['IP_RATE_LIMIT'])
)

CREATE_EMAIL_ERROR_MESSAGE = 'Exceeded limit for same email address: {}'.format(
    limits.parse(app.config['CREATE_EMAIL_RATE_LIMIT'])
)

REQUEST_DELETE_ERROR_MESSAGE = 'Exceeded limit for same email address: {}'.format(
    limits.parse(app.config['REQUEST_DELETE_RATE_LIMIT'])
)

@app.route('/api/new', methods=['POST'])
@ip_limiter.limit(app.config['IP_RATE_LIMIT'],
                 get_remote_address,
                 error_message=IP_ERROR_MESSAGE)
@email_limiter.limit(app.config['CREATE_EMAIL_RATE_LIMIT'],
                    get_email_from_request,
                    error_message=CREATE_EMAIL_ERROR_MESSAGE)
def new():
    data = request.get_json(force=True)
    if 'email' not in data:
        return dict(
            status='ERROR',
            reason='Email missing'
        ), status.HTTP_400_BAD_REQUEST
    if data['email'].endswith(app.config['EMAIL_POSTFIX']):
        return dict(
            status='ERROR',
            reason='Forwarding to this domain is not allowed'
        ), status.HTTP_400_BAD_REQUEST
    match = re.match(EMAIL_REGEX, data['email'])
    if not match:
        return dict(
            status='ERROR',
            reason='Invalid email address'
        ), status.HTTP_400_BAD_REQUEST
    dictionary_path = app.config['BEAUTIFURL_DICTIONARIES_URI']
    beautifurl = Beautifurl(dictionary_path=dictionary_path)
    emails = beautifurl.get_permutations(app.config['BEAUTIFURL_FORMAT'], shuffle=True)
    for email in emails:
        email = email + app.config['EMAIL_POSTFIX']
        try:
            alias = VirtualAlias(
                alias_email=email,
                real_email=request.get_json()['email']
            )
            db.session.add(alias)
            db.session.commit()
            return dict(
                status='OK',
                email=email
            ), status.HTTP_201_CREATED
        except (InvalidRequestError, IntegrityError):
            db.session.rollback()
    return dict(
        status='ERROR',
        reason='Addresses exhausted.  Please inform an administrator.'
    ), status.HTTP_500_INTERNAL_SERVER_ERROR

@app.route('/api/delete', methods=['POST'])
def delete():
    data = request.get_json(force=True)
    if ('email' not in data
            or 'timestamp' not in data
            or 'token' not in data):
        return dict(
            status='ERROR',
            reason='Missing arguments'
        ), status.HTTP_400_BAD_REQUEST
    verification_token = generate_token(data['email'],
                                        timestamp=data['timestamp'])
    if verification_token != data['token']:
        return dict(
            status='ERROR',
            reason='Invalid token'
        ), status.HTTP_400_BAD_REQUEST
    if int(data['timestamp']) + app.config['DELETE_TOKEN_EXPIRY'] < time.time():
        return dict(
            status='ERROR',
            reason='Token expired'
        ), status.HTTP_400_BAD_REQUEST
    alias = VirtualAlias.query.filter_by(
        alias_email=data['email'],
        enabled=True
    ).first()
    if alias is None:
        return dict(
            status='ERROR',
            reason='Email address not found'
        ), status.HTTP_400_BAD_REQUEST
    alias.enabled = False
    db.session.commit()
    return dict(
        status='OK',
    ), status.HTTP_200_OK

@app.route('/api/request_delete', methods=['POST'])
@ip_limiter.limit(app.config['IP_RATE_LIMIT'],
                 get_remote_address,
                 error_message=IP_ERROR_MESSAGE)
@email_limiter.limit(app.config['REQUEST_DELETE_RATE_LIMIT'],
                    get_email_from_request,
                    error_message=REQUEST_DELETE_ERROR_MESSAGE)
def request_delete():
    data = request.get_json(force=True)
    if 'email' not in data:
        return dict(
            status='ERROR',
            reason='Missing arguments'
        ), status.HTTP_400_BAD_REQUEST
    alias = VirtualAlias.query.filter_by(
        alias_email=data['email'],
        enabled=True
    ).first()
    if alias is None:
        return dict(
            status='ERROR',
            reason='Email address not found'
        ), status.HTTP_400_BAD_REQUEST
    link = generate_delete_link(data['email'])
    body = app.config['MAIL_DELETE_REQUEST_BODY'].format(
        email=data['email'],
        link=link
    )
    msg = Message(subject=app.config['MAIL_DELETE_REQUEST_SUBJECT'],
                  sender=app.config['MAIL_SENDER'],
                  recipients=[data['email']],
                  body=body
                 )
    if app.config['DEBUG']:
        print(msg)
    else:
        mail.send(msg)
    return dict(
        status='OK',
    ), status.HTTP_200_OK

def generate_token(email, timestamp=None):
    hasher = hashlib.sha256()
    hasher.update(app.config['SECRET_KEY'].encode('utf-8'))
    hasher.update(email.encode('utf-8'))
    if timestamp is not None:
        hasher.update(str(timestamp).encode('utf-8'))
    else:
        hasher.update(str(int(time.time())).encode('utf-8'))
    return hasher.hexdigest()

def generate_delete_link(email):
    timestamp = str(int(time.time()))
    token = generate_token(email, timestamp=timestamp)
    link = 'https://shadowmail.co.uk/delete?'
    link += 'email=' + email
    link += '&timestamp=' + timestamp
    link += '&token=' + token
    return link
