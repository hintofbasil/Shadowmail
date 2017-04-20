from main import app, db
from models.virtual_alias import VirtualAlias
from sqlalchemy.exc import InvalidRequestError, IntegrityError

from flask import request
from flask_api import status

from beautifurl import Beautifurl
import math
import random

@app.route('/new', methods=['POST'])
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
