from flask import Blueprint, request # type: ignore
from src.app import User, db
from http import HTTPStatus
from sqlalchemy import inspect # type: ignore
from flask_jwt_extended import jwt_required # type: ignore
from src.utils import requires_role
from src.app import bcrypt
from src.views.user import UserSchema, CreateUserSchema, GetUserParameter
from marshmallow import ValidationError

app = Blueprint('user', __name__, url_prefix='/users')

def _create_user():
    user_schema = CreateUserSchema()

    try:
        data = user_schema.load(request.json)
    except ValidationError as exc:
        return exc.messages, HTTPStatus.UNPROCESSABLE_ENTITY

    user = User(
        username=data["username"],
        password=bcrypt.generate_password_hash(data["password"]),
        role_id=data["role_id"],
        )
    db.session.add(user)
    db.session.commit()
    return {'message': 'User Created!'}, HTTPStatus.CREATED


@jwt_required()
@requires_role('admin')
def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars()

    users_schema = UserSchema(many=True)
    return users_schema.dump(users)

    # return [
    #     {
    #         "id": user.id,
    #         "username": user.username,
    #         "role":{
    #             "id": user.role.id,
    #             "name": user.role.name
    #         }
    #     }
    #     for user in users
    # ]

@app.route('/', methods=['GET', 'POST'])
def handle_user():
    """
    User collection operations.
    ---
    get:
      tags:
        - User
      summary: List all users
      responses:
        200:
          description: List of users
          content:
            application/json:
              schema:
                type: object
                properties:
                  users:
                    type: array
                    items: UserSchema
    post:
      tags:
        - User
      summary: Create a user
      requestBody:
        required: true
        content:
          application/json:
            schema: CreateUserSchema
      responses:
        201:
          description: User Created!
    """
    if request.method == 'POST':
        return _create_user()
    else:
        return {'users': _list_users()}


@app.route('/<int:user_id>')
# @jwt_required()
# @requires_role('admin')
def get_user(user_id):
    """
    User detail view.
    ---
    get:
      tags:
        - User
      summary: Get a user by ID
      parameters:
        - in: path
          name: user_id
          schema: GetUserParameter

      responses:
        200:
          description: Successful operation
          content:
            application/json:
              schema: UserSchema
    """
        
    user = db.get_or_404(User, user_id)
    return {
        "id": user.id,
        "username": user.username,
    }

@app.route('/<int:user_id>', methods=["PATCH"])
# @jwt_required()
# @requires_role('admin')
def update_user(user_id):
    """
    Update user information.
    ---
    patch:
      tags:
        - User
      summary: Update a user by ID
      parameters:
        - in: path
          name: user_id
          required: true
          schema: {type: integer}
      requestBody:
        content:
          application/json:
            schema: UserSchema
      responses:
        200:
          description: Successful operation
    """
    user = db.get_or_404(User, user_id)
    data = request.json
    
    mapper = inspect(User)
    for column in mapper.attrs:
        if column.key in data:
            setattr(user, column.key, data[column.key])
    db.session.commit()
    
    return {
        "id": user.id,
        "username": user.username,
    }

@app.route('/<int:user_id>', methods=["DELETE"])
# @jwt_required()
# @requires_role('admin')
def delete_user(user_id):
    """
    Delete a user.
    ---
    delete:
      tags:
        - User
      summary: Remove a user by ID
      parameters:
        - in: path
          name: user_id
          required: true
          schema: {type: integer}
      responses:
        204:
          description: No Content
    """
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT