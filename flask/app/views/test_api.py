from main import app, db, emailLimiter, ipLimiter, mail
from models.virtual_alias import VirtualAlias
from views.api import generate_token
from flask_api import status

from beautifurl import Beautifurl
import hashlib
import json
import limits
import pytest
import re
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

@pytest.fixture()
def reset_limits(request):
    def reset_client_limits():
        emailLimiter.reset()
        ipLimiter.reset()
    request.addfinalizer(reset_client_limits)

def create_email_alias(prefix=None):
    client = app.test_client()
    if prefix is not None:
        email = str(prefix) + '@example.com'
    else:
        email = 'test@example.com'
    data = dict(
        email=email
    )
    data = json.dumps(data)
    response = client.post('/new', data=data,
                          content_type='application/json')
    return response

def test_new_email_get_invalid(set_up_client, reset_limits):
    client = app.test_client()
    response = client.get('/new')
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_new_email_arg_missing(set_up_client, reset_limits):
    client = app.test_client()
    data = dict()
    data = json.dumps(data)
    response = client.post('/new', data=data,
                          content_type='application/json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_generate_valid_email(set_up_client, reset_limits):
    response = create_email_alias()
    assert response.status_code == status.HTTP_201_CREATED
    jsonData = json.loads(response.get_data())
    assert jsonData['email'].endswith(app.config['EMAIL_POSTFIX'])
    assert '\n' not in jsonData['email']

def test_email_saved_in_database(set_up_client, reset_limits, clear_db):
    response = create_email_alias()
    assert response.status_code == status.HTTP_201_CREATED
    jsonData = json.loads(response.get_data())
    aliases = VirtualAlias.query.all()
    assert len(aliases) == 1
    assert aliases[0].alias_email == jsonData['email']
    assert aliases[0].real_email == 'test@example.com'
    assert aliases[0].enabled == True

def test_email_all_permutations_exhuasted(set_up_client, reset_limits, clear_db):
    dictionaryPath = app.config['BEAUTIFURL_DICTIONARIES_URI']
    # Need to reduce permutations to avoid ip rate limiting
    app.config['BEAUTIFURL_FORMAT'] = 'ww'
    beautifurl = Beautifurl(dictionaryPath=dictionaryPath)
    perms = beautifurl.count_permutations(app.config['BEAUTIFURL_FORMAT'])
    for i in range(perms): # Generate all possible emails
        create_email_alias(i)
    aliases = VirtualAlias.query.all()
    assert len(aliases) == perms
    response = create_email_alias()
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert len(aliases) == perms

def test_delete_email_get_invalid(set_up_client, reset_limits):
    client = app.test_client()
    response = client.get('/delete')
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_delete_token_incorrect(set_up_client, reset_limits):
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

def test_delete_expired(set_up_client, reset_limits):
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

def test_invalid_email(set_up_client, reset_limits):
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

def test_valid_delete(set_up_client, reset_limits, clear_db):
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

def test_double_delete(set_up_client, reset_limits, clear_db):
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

def test_request_delete_get_invalid(set_up_client, reset_limits):
    client = app.test_client()
    response = client.get('/request_delete')
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_request_delete_user_doesnt_exist(set_up_client, reset_limits):
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

def test_request_delete_user_disabled(set_up_client, reset_limits, clear_db):
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

def test_request_delete_email_created(set_up_client, reset_limits, clear_db):
    response = create_email_alias()
    assert len(VirtualAlias.query.all()) == 1
    jsonData = json.loads(response.get_data())
    email = jsonData['email']

    client = app.test_client()
    data = dict(
        email=email,
    )
    data = json.dumps(data)
    with mail.record_messages() as outbox:
        response = client.post('/request_delete', data=data,
                               content_type='application/json')
        assert response.status_code == status.HTTP_200_OK
        assert 'OK' in str(response.data)
        assert len(outbox) == 1
        msg = outbox[0]
        assert msg.subject == app.config['MAIL_DELETE_REQUEST_SUBJECT']
        assert msg.sender == app.config['MAIL_SENDER']
        assert msg.recipients == [email]
        link_regex = r'https://(www)?shadowmail\.co\.uk/delete\?email=' + email
        link_regex += r'&time=\d{10}&token=[0-9a-f]{64}'
        m = re.compile(link_regex)
        assert m.search(msg.body) is not None

def test_create_rate_limit_ip(set_up_client, reset_limits, clear_db):
    limit = int(app.config['IP_RATE_LIMIT'].split('/')[0])
    # Need to extend possibilities to hit rate limit
    app.config['BEAUTIFURL_FORMAT'] = 'www'
    for i in range(limit):
        response = create_email_alias(prefix=i)
        assert response.status_code == status.HTTP_201_CREATED
    response = create_email_alias()
    assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
    assert 'Exceeded limit from same ip address' in str(response.data)
    limit = str(limits.parse(app.config['IP_RATE_LIMIT']))
    assert limit in str(response.data)

def test_request_delete_rate_limit_ip(set_up_client, reset_limits, clear_db):
    client = app.test_client()
    limit = int(app.config['IP_RATE_LIMIT'].split('/')[0])
    for i in range(limit):
        # Ensure each email unique to avoid email rate limit
        # Binary just for fun
        data = dict(
            email='{0:b}@shadowmail.co.uk'.format(i),
        )
        data = json.dumps(data)
        response = client.post('/request_delete', data=data,
                               content_type='application/json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'Email address not found' in str(response.data)
    data = dict(
        email='{0:b}@shadowmail.co.uk'.format(i + 1),
    )
    data = json.dumps(data)
    response = client.post('/request_delete', data=data,
                           content_type='application/json')
    assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
    assert 'Exceeded limit from same ip address' in str(response.data)
    limit = str(limits.parse(app.config['IP_RATE_LIMIT']))
    assert limit in str(response.data)

def test_create_rate_limit_email(set_up_client, reset_limits, clear_db):
    limit = int(app.config['CREATE_EMAIL_RATE_LIMIT'].split('/')[0])
    ipLimit = int(app.config['IP_RATE_LIMIT'].split('/')[0])
    # Must hit email limit first
    assert limit < ipLimit
    # Need to extend possibilities to hit rate limit
    app.config['BEAUTIFURL_FORMAT'] = 'www'
    for _ in range(limit):
        response = create_email_alias()
        assert response.status_code == status.HTTP_201_CREATED
    response = create_email_alias()
    assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
    assert 'Exceeded limit for same email address' in str(response.data)
    limit = str(limits.parse(app.config['CREATE_EMAIL_RATE_LIMIT']))
    assert limit in str(response.data)

def test_request_delete_limit_email(set_up_client, reset_limits, clear_db):
    client = app.test_client()
    limit = int(app.config['CREATE_EMAIL_RATE_LIMIT'].split('/')[0])
    ipLimit = int(app.config['IP_RATE_LIMIT'].split('/')[0])
    # Must hit email limit first
    assert limit < ipLimit
    response = create_email_alias()
    data = json.loads(response.data)
    email = data['email']
    assert response.status_code == status.HTTP_201_CREATED
    # Legitimate request
    data = dict(
        email=email,
    )
    data = json.dumps(data)
    response = client.post('/request_delete', data=data,
                           content_type='application/json')
    assert response.status_code == status.HTTP_200_OK
    #Double request
    data = dict(
        email=email,
    )
    data = json.dumps(data)
    response = client.post('/request_delete', data=data,
                           content_type='application/json')
    assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
    assert 'Exceeded limit for same email address' in str(response.data)
    limit = str(limits.parse(app.config['REQUEST_DELETE_RATE_LIMIT']))
    assert limit in str(response.data)
