from main import app, db, limiter, mail
from models.virtual_alias import VirtualAlias
from sqlalchemy.exc import InvalidRequestError, IntegrityError

from flask import request
from flask_api import status
from flask_mail import Message
from flask_limiter.util import get_remote_address

from beautifurl import Beautifurl
import limits
import hashlib
import math
import random
import time

ip_error_message = 'Exceeded limit from same ip address: %s'.format(
    limits.parse(app.config['IP_RATE_LIMIT'])
)

@app.route('/new', methods=['POST'])
@limiter.limit(app.config['IP_RATE_LIMIT'],
                 get_remote_address,
                 error_message=ip_error_message)
def new():
    if 'email' not in request.get_json(force=True):
        return dict(
            status='Email missing'
        ), status.HTTP_400_BAD_REQUEST
    dictionaryPath = app.config['BEAUTIFURL_DICTIONARIES_URI']
    beautifurl = Beautifurl(dictionaryPath=dictionaryPath)
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
    ), status.HTTP_500_INTERNAL_SERVER_ERROR

@app.route('/delete', methods=['POST'])
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
    if data['timestamp'] + app.config['DELETE_TOKEN_EXPIRY'] < time.time():
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

@app.route('/request_delete', methods=['POST'])
@limiter.limit(app.config['IP_RATE_LIMIT'],
                 get_remote_address,
                 error_message=ip_error_message)
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
    body=app.config['MAIL_DELETE_REQUEST_BODY'].format(
        email=data['email'],
        link=link
    )
    msg = Message(subject=app.config['MAIL_DELETE_REQUEST_SUBJECT'],
                  sender=app.config['MAIL_SENDER'],
                  recipients=[data['email']],
                  body=body
                 )
    mail.send(msg)
    return dict(
        status='OK',
    ), status.HTTP_200_OK

def generate_token(email, timestamp=None):
    m = hashlib.sha256()
    m.update(app.config['SECRET_KEY'].encode('utf-8'))
    m.update(email.encode('utf-8'))
    if timestamp is not None:
        m.update(str(timestamp).encode('utf-8'))
    else:
        m.update(str(int(time.time())).encode('utf-8'))
    return m.hexdigest()

def generate_delete_link(email):
    timestamp = str(int(time.time()))
    token = generate_token(email, timestamp=timestamp)
    link = 'https://shadowmail.co.uk/delete/?'
    link += 'email=' + email
    link += '&time=' + timestamp
    link += '&token=' + token
    return link
