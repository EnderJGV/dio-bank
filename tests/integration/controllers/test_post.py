from http import HTTPStatus
from src.app import Post, User, Role, db

# Test do Get
def test_get_posts(client):
    # Given
    # Criamos a estrutura necessária: Role -> User -> Post
    role = Role(name='admin')
    db.session.add(role)
    db.session.commit()

    user = User(username='author', password='123', role_id=role.id)
    db.session.add(user)
    db.session.commit()

    post = Post(title="Test Title", body="Test Body", author_id=user.id)
    db.session.add(post)
    db.session.commit()

    # When
    response = client.get('/posts/listPosts')

    exported_data = {
        "posts": [
            {
                "id": post.id,
                "title": post.title,
                "body": post.body,
                "created_at": post.created.isoformat(),
                "author_id": post.author_id
            }
        ]
    }

    # Then
    assert response.status_code == HTTPStatus.OK
    assert response.json == exported_data

# Test do Post
def test_create_post(client):
    # Given
    payload = {
        "title": "Test Post",
        "body": "This is a test post",
        "author_id": 1
    }

    # When
    response = client.post('posts/create', json=payload)
    
    # Then 
    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {
        "message": "Post Created!"
    }

# Teste do Patch
def test_update_post(client):
    # Given
    # Criamos a estrutura necessária: Role -> User -> Post
    role = Role(name='admin')
    db.session.add(role)
    db.session.commit()

    user = User(username='author', password='123', role_id=role.id)
    db.session.add(user)
    db.session.commit()

    post = Post(title="Test Title", body="Test Body", author_id=user.id)
    db.session.add(post)
    db.session.commit()

    payload = {
        "title": "Titulo Atualizado"
    }

    response = client.patch(f'/posts/updateInformationPost/{post.id}', json=payload)

    # Then 
    assert response.status_code == HTTPStatus.OK
    assert post.title == "Titulo Atualizado"
    assert post.body == "Test Body"
    assert response.json == {
        "id": post.id,
        "title": post.title,
        "body": post.body,
        "created_at": post.created.isoformat(),
        "author_id": post.author_id,
        "message": "Post Updated!"
    }

# Teste do Delete
def test_delete_post(client):
    # Given
    role = Role(name='admin')
    db.session.add(role)
    db.session.commit()

    user = User(username='deleter', password='123', role_id=role.id)
    db.session.add(user)
    db.session.commit()

    post = Post(title="Post para Deletar", body="Será removido", author_id=user.id)
    db.session.add(post)
    db.session.commit()

    post_id = post.id

    # When
    response = client.delete(f'/posts/deletePost/{post_id}')

    # Then
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert db.session.get(Post, post_id) is None
