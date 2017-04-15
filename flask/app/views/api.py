from main import app, db
from models.virtual_alias import VirtualAlias
from sqlalchemy.exc import InvalidRequestError, IntegrityError

from flask import request
from flask_api import status

from lazysorted import LazySorted
import math
import random

@app.route('/new', methods=['POST'])
def new():
    if 'email' not in request.get_json():
        return dict(
            status='Email missing'
        ), status.HTTP_400_BAD_REQUEST
    emails = generate_emails()
    for email in emails:
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

def load_wordlist():
    # Not sure if can return in a with block
    ret = []
    with open(app.config['WORD_LIST_URI'], 'r') as f:
        return f.readlines()

# Taken from http://stackoverflow.com/a/5602615
def generate_nth_permutation(words, n):
    words = words[:]
    for i in range(len(words)-1):
        n, j = divmod(n, len(words)-i)
        words[i], words[i+j] = words[i+j], words[i]
    return words

def generate_emails():
    words = load_wordlist()
    perms = math.factorial(len(words))
    for i in LazySorted(range(perms)):
        permutation = generate_nth_permutation(words, i)
        email = ''.join(permutation) + app.config['EMAIL_POSTFIX']
        yield email.lower().replace('\n', '')
