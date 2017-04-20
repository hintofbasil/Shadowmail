from main import app, db
from models.virtual_alias import VirtualAlias
from flask_api import status

from beautifurl import Beautifurl
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
