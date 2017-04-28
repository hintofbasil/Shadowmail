from main import app
from flask_api import status

def test_homepage_get():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK
