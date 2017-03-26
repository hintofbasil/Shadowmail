from main import app, db
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
    assert response.status_code == 405
