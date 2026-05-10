import pytest
from src.app import create_app, db, User, Role

@pytest.fixture
def app():
    app = create_app(
        enviroment="testing"
    )
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def access_token(client):
        # Given
    # Isso faz o insert da role para atribuir ao user
    role = Role(name='admin')
    db.session.add(role)
    db.session.commit()

    # Isso faz o insert do user
    user = User(username='john-doe', password='test', role_id=role.id)
    db.session.add(user)
    db.session.commit()

    response = client.post('auth/login', json={
        "username": user.username,
        "password": user.password
    })
    access_token = response.json['access_token']
    return access_token
