from flask_api import status

from main import app

def test_homepage_get():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK

def test_request_delete_get():
    client = app.test_client()
    response = client.get('/request_delete')
    assert response.status_code == status.HTTP_200_OK
