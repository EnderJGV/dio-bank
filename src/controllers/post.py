from sqlalchemy import inspect
from flask import Blueprint, request
from src.app import Post, db
from http import HTTPStatus
from datetime import datetime

app = Blueprint('post', __name__, url_prefix='/posts')

def _create_post():
    data = request.json
    post = Post(title=data["title"], body=data["body"], author_id=data["author_id"])
    db.session.add(post)
    db.session.commit()

def _list_posts():
    query = db.select(Post)
    posts = db.session.execute(query).scalars() #.scalars() para retornar os objetos Post ao invés de tuplas
    return [
        {
            "id": post.id,
            "title": post.title,
            "body": post.body,
            "created_at": post.created.isoformat(),
            "author_id": post.author_id
        }
        for post in posts
    ]

# CRUD - Create, Read, Update, Delete


# Create
@app.route('/create', methods=["POST"])
def create_post():
    """
    Create a new post.
    ---
    post:
      tags:
        - Post
      summary: Create a new post
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                title: {type: string}
                body: {type: string}
                author_id: {type: integer}
      responses:
        201:
          description: Post Created!
    """
    _create_post()
    return{
        "message": "Post Created!"
    }, HTTPStatus.CREATED

#Read
@app.route("listPosts", methods=["GET"])
def get_posts():
    """
    List all posts.
    ---
    get:
      tags:
        - Post
      summary: Get all posts
      responses:
        200:
          description: A list of posts
    """
    return {
        "posts": _list_posts()
    }, HTTPStatus.OK

# Update
@app.route('/updateInformationPost/<int:post_id>', methods=["PATCH"])
def update_post(post_id):
    """
    Update post information.
    ---
    patch:
      tags:
        - Post
      summary: Update a post by ID
      parameters:
        - in: path
          name: post_id
          required: true
          schema: {type: integer}
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                title: {type: string}
                body: {type: string}
      responses:
        200:
          description: Post Updated!
    """
    post = db.get_or_404(Post, post_id)
    data = request.json

    mapper = inspect(Post)
    for column in mapper.attrs:
        if column.key in data:
            setattr(post, column.key, data[column.key])
    db.session.commit()

    return {
        "id": post.id,
        "title": post.title,
        "body": post.body,
        "created_at": post.created.isoformat(),
        "author_id": post.author_id,
        "message": "Post Updated!"
    }, HTTPStatus.OK

@app.route('/deletePost/<int:post_id>', methods=["DELETE"])
def delete_post(post_id):
    """
    Delete a post.
    ---
    delete:
      tags:
        - Post
      summary: Remove a post by ID
      parameters:
        - in: path
          name: post_id
          required: true
          schema: {type: integer}
      responses:
        204:
          description: No Content
    """
    post = db.get_or_404(Post, post_id)
    db.session.delete(post)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT