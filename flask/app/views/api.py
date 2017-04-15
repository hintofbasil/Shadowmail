from main import app

from flask import request
from flask_api import status

@app.route('/new', methods=['POST'])
def new():
    if 'email' not in request.get_json():
        return dict(
            status = 'Email missing'
        ), status.HTTP_400_BAD_REQUEST
    return dict(
        status = 'OK'
    )
