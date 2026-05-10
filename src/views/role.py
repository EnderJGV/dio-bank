from src.app import ma
from src.models import Role

class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Role
        include_fk = True
        load_instance = True
        fields = ("id", "name")