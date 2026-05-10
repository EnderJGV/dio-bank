from src.app import ma
from src.models import User
from src.views.role import RoleSchema
from marshmallow import fields

class UserSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = User
        load_instance = True
        include_fk = True
        fields = ("id", "username", "role")

    role = ma.Nested(RoleSchema)

class GetUserParameter(ma.Schema):
    user_id = fields.Integer(required=True, strict=True)

class CreateUserSchema(ma.Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
    role_id = fields.Integer(required=True, strict=True)