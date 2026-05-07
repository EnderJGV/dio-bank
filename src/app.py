import os

import sqlalchemy as sa

from flask import Flask
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from src.models.base import db
from src.models.post import Post
from src.models.role import Role

migrate = Migrate()
jwt = JWTManager()

class User(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(sa.String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(sa.String, nullable=False)
    role_id: Mapped[int] = mapped_column(sa.ForeignKey('role.id'))
    role: Mapped['Role'] = relationship(back_populates='user') 

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r})"


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI="sqlite:///blog.sqlite",
        JWT_SECRET_KEY="super-secret",
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)


    # a simple page that says hello
    # @app.route('/hello')
    # def hello():
    #     return 'Hello, World!'

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Register BluePrint
    from src.controllers import user, post, auth, role

    app.register_blueprint(user.app)
    app.register_blueprint(post.app)
    app.register_blueprint(auth.app)
    app.register_blueprint(role.app)

    return app