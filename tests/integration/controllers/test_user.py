from http import HTTPStatus
from src.app import Role, User, db
from sqlalchemy import func

def test_get_user_sucess(client):
    # Given
    # Isso faz o insert da role para atribuir ao user
    role = Role(name='admin')
    db.session.add(role)
    db.session.commit()

    # Isso faz o insert do user
    user = User(username='john-doe', password='test', role_id=role.id)
    db.session.add(user)
    db.session.commit()

    # When
    # Faz a requisição para o endpoint de get_user e valida se o status code e o retorno estão corretos
    response = client.get(f'/users/{user.id}')

    # Then
    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "id": user.id,
        "username": user.username,
    }

def test_get_user_not_found(client):
    # Given
    # Isso faz o insert da role para atribuir ao user
    role = Role(name='admin')
    db.session.add(role)
    db.session.commit()

    user_id = 1

    # When
    # Faz a requisição para o endpoint de get_user e valida se o status code e o retorno estão corretos
    response = client.get(f'/users/{user_id}')

    # Then
    assert response.status_code == HTTPStatus.NOT_FOUND

def test_create_user(client, access_token):

    role_id = db.session.execute(db.select(Role.id).where(Role.name == 'admin')).scalar()

    payload = {
        "username": "jane-doe",
        "password": "test",
        "role_id": role_id
    }

    # When
    response = client.post('/users/', json=payload, headers={'Authorization': f'Bearer {access_token}'})

    # Then
    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {'message': 'User Created!'}
    assert db.session.execute(db.select(func.count(User.id))).scalar() == 2


def test_list_users(client, access_token):
    # Given
    user = db.session.execute(db.select(User).where(User.username == 'john-doe')).scalar()

    response = client.post('auth/login', json={
        "username": user.username,
        "password": user.password
    })
    access_token = response.json['access_token']

    # When
    respose = client.get('/users/', headers={'Authorization': f'Bearer {access_token}'})

    # Then
    assert respose.status_code == HTTPStatus.OK
    assert respose.json == {
        "users": [
            {
                "id": user.id,
                "username": user.username,
                "role":{
                    "id": user.role.id,
                    "name": user.role.name
                }
            }
        ]
    }