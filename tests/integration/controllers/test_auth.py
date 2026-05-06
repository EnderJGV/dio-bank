from http import HTTPStatus
from src.app import Role, User, db

# Test Login
def test_login(client):
    # Given
    role = Role(name='admin')
    db.session.add(role)
    db.session.commit()

    user = User(username='admin', password='admin', role_id=role.id)
    db.session.add(user)
    db.session.commit()

    payload = {
        "username": "admin",
        "password": "admin"
    }

    # When
    response = client.post('auth/login', json=payload)

    # Then
    assert response.status_code == HTTPStatus.OK
    assert "access_token" in response.json