from main import app, db
from models.virtual_alias import VirtualAlias
from views.api import generate_token
from flask_api import status

from beautifurl import Beautifurl
import hashlib
import json
import pytest
import time

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

@pytest.fixture()
def clear_db(request):
    db.drop_all()
    db.configure_mappers()
    db.create_all()
    db.session.commit()

def create_email_alias():
    client = app.test_client()
    data = dict(
        email='test@example.com'
    )
    data = json.dumps(data)
    response = client.post('/new', data=data,
                          content_type='application/json')
    return response

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
    response = create_email_alias()
    assert response.status_code == status.HTTP_201_CREATED
    jsonData = json.loads(response.get_data())
    assert jsonData['email'].endswith(app.config['EMAIL_POSTFIX'])
    assert '\n' not in jsonData['email']

def test_email_saved_in_database(set_up_client, clear_db):
    response = create_email_alias()
    assert response.status_code == status.HTTP_201_CREATED
    jsonData = json.loads(response.get_data())
    aliases = VirtualAlias.query.all()
    assert len(aliases) == 1
    assert aliases[0].alias_email == jsonData['email']
    assert aliases[0].real_email == 'test@example.com'
    assert aliases[0].enabled == True

def test_email_all_permutations_exhuasted(set_up_client, clear_db):
    dictionaryPath = app.config['BEAUTIFURL_DICTIONARIES_URI']
    beautifurl = Beautifurl(dictionaryPath=dictionaryPath)
    perms = beautifurl.count_permutations(app.config['BEAUTIFURL_FORMAT'])
    for i in range(perms): # Generate all possible emails
        create_email_alias()
    aliases = VirtualAlias.query.all()
    assert len(aliases) == perms
    response = create_email_alias()
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert len(aliases) == perms

def test_delete_email_get_invalid(set_up_client):
    client = app.test_client()
    response = client.get('/delete')
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_delete_token_incorrect(set_up_client):
    client = app.test_client()
    m = hashlib.sha256()
    m.update(app.config['SECRET_KEY'].encode('utf-8'))
    data = dict(
        email='test@example.com',
        timestamp=time.time(),
        token=m.hexdigest()
    )
    data = json.dumps(data)
    response = client.post('/delete', data=data,
                          content_type='application/json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'Invalid token' in str(response.data)

def test_delete_expired(set_up_client):
    client = app.test_client()
    email = 'test@example.com'
    timestamp = int(time.time()) - app.config['DELETE_TOKEN_EXPIRY'] - 1
    token = generate_token(email, timestamp=timestamp)
    data = dict(
        email=email,
        timestamp=timestamp,
        token=token
    )
    data = json.dumps(data)
    response = client.post('/delete', data=data,
                          content_type='application/json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'Token expired' in str(response.data)

def test_invalid_email(set_up_client):
    client = app.test_client()
    email = 'test@example.com'
    timestamp = int(time.time())
    token = generate_token(email, timestamp=timestamp)
    data = dict(
        email=email,
        timestamp=timestamp,
        token=token
    )
    data = json.dumps(data)
    response = client.post('/delete', data=data,
                          content_type='application/json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'Email address not found' in str(response.data)

def test_valid_delete(set_up_client, clear_db):
    response = create_email_alias()
    assert len(VirtualAlias.query.all()) == 1
    jsonData = json.loads(response.get_data())
    email = jsonData['email']

    client = app.test_client()
    timestamp = int(time.time())
    token = generate_token(email, timestamp=timestamp)
    data = dict(
        email=email,
        timestamp=timestamp,
        token=token
    )
    data = json.dumps(data)
    response = client.post('/delete', data=data,
                          content_type='application/json')
    assert response.status_code == status.HTTP_200_OK
    assert 'OK' in str(response.data)
    assert len(VirtualAlias.query.all()) == 1
    assert VirtualAlias.query.get(1).enabled == False

def test_double_delete(set_up_client, clear_db):
    response = create_email_alias()
    assert len(VirtualAlias.query.all()) == 1
    jsonData = json.loads(response.get_data())
    email = jsonData['email']

    client = app.test_client()
    timestamp = int(time.time())
    token = generate_token(email, timestamp=timestamp)
    data = dict(
        email=email,
        timestamp=timestamp,
        token=token
    )
    data = json.dumps(data)
    client.post('/delete', data=data,
                content_type='application/json')
    response = client.post('/delete', data=data,
                           content_type='application/json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'Email address not found' in str(response.data)

def test_request_delete_get_invalid(set_up_client):
    client = app.test_client()
    response = client.get('/request_delete')
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_request_delete_user_doesnt_exist(set_up_client):
    client = app.test_client()
    email = 'test@example.com'
    data = dict(
        email=email,
    )
    data = json.dumps(data)
    response = client.post('/request_delete', data=data,
                           content_type='application/json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'Email address not found' in str(response.data)

def test_request_delete_user_disabled(set_up_client, clear_db):
    response = create_email_alias()
    assert len(VirtualAlias.query.all()) == 1
    jsonData = json.loads(response.get_data())
    email = jsonData['email']

    VirtualAlias.query.get(1).enabled = False
    db.session.commit()
    assert VirtualAlias.query.get(1).enabled == False

    client = app.test_client()
    data = dict(
        email=email,
    )
    data = json.dumps(data)
    response = client.post('/request_delete', data=data,
                           content_type='application/json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'Email address not found' in str(response.data)
