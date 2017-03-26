from main import app

from flask import request

@app.route('/new', methods=['POST'])
def test():
    return "Hello world!"
