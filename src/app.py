import os

from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

# from src.models.base import db
# from src.models.post import Post
# from src.models.role import Role
# from src.models.user import User

from src.models import db, Post, Role, User

migrate = Migrate()
jwt = JWTManager()


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