from flask import Blueprint, request
from src.app import Role, db
from http import HTTPStatus

app = Blueprint('role', __name__, url_prefix='/roles')

@app.route('/', methods=['POST'])
def create_role():
    """
    Create a new role.
    ---
    post:
      tags:
        - Role
      summary: Create a role
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                name: {type: string}
      responses:
        201:
          description: Role Created!
    """
    data = request.json
    role = Role(name=data["name"])
    db.session.add(role)
    db.session.commit()
    return {
        "message": "Role Created!"
    }, HTTPStatus.CREATED
