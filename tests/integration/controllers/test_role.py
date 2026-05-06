from http import HTTPStatus
from src.app import Role, db

# Test role creation
def test_create_role(client):
    # Given
    payload = {
        "name": "roleTest"
    }

    # When
    response = client.post('/roles/', json=payload)

    # Then
    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {
        "message": "Role Created!"
    }
    assert db.session.query(Role).filter_by(name="roleTest").first() is not None

