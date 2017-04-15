from main import app

from flask import request
from flask_api import status

import random

@app.route('/new', methods=['POST'])
def new():
    if 'email' not in request.get_json():
        return dict(
            status='Email missing'
        ), status.HTTP_400_BAD_REQUEST
    email = generate_email()
    return dict(
        status='OK',
        email=email
    ), status.HTTP_201_CREATED

def load_wordlist():
    # Not sure if can return in a with block
    ret = []
    with open(app.config['WORD_LIST_URI'], 'r') as f:
        return f.readlines()

def generate_random_words():
    words = load_wordlist()
    generated = []
    max = app.config['EMAIL_WORD_COUNT']
    # Swaps last element with used element
    # to make algorithm O(n)
    while max > 0:
        max = max - 1
        index = random.randint(0, len(words) - 1)
        generated.append(words[index])
        words[index] = words[-1]
        del words[-1]
    return generated

def generate_email():
    words = generate_random_words()
    email = ''.join(words) + app.config['EMAIL_POSTFIX']
    return email.lower().replace('\n', '')
