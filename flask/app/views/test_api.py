from main import app, db
from flask_api import status

import json
import pytest

@pytest.fixture(scope='module')
def set_up_client(request):
    app_context = app.app_context()
    app_context.push()
    def tear_down_client():
        db.drop_all()
        db.configure_mappers()
        db.create_all()
        db.session.commit()

        app_context.pop()
    request.addfinalizer(tear_down_client)

def test_new_email_get_invalid(set_up_client):
    client = app.test_client()
    response = client.get('/new')
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_new_email_arg_missing(set_up_client):
    client = app.test_client()
    data = dict()
    data = json.dumps(data)
    response = client.post('/new', data=data,
                          content_type='application/json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_generate_valid_email(set_up_client):
    client = app.test_client()
    data = dict(
        email='test@example.com'
    )
    data = json.dumps(data)
    response = client.post('/new', data=data,
                          content_type='application/json')
    assert response.status_code == status.HTTP_201_CREATED
    jsonData = json.loads(response.get_data())
    assert jsonData['email'].endswith(app.config['EMAIL_POSTFIX'])
    assert '\n' not in jsonData['email']
