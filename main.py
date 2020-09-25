from flask import Flask
from flask_jwt_extended import JWTManager

from api.utils.database import db
from api.utils.email import mail
from api.config.config import config

jwt = JWTManager()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    jwt.init_app(app)
    db.init_app(app)
    mail.init_app(app)

    from api.routes.users import user_routes
    app.register_blueprint(user_routes, url_prefix='/api/users')

    from api.routes.authors import author_routes
    app.register_blueprint(author_routes, url_prefix='/api/authors')

    from api.routes.books import book_routes
    app.register_blueprint(book_routes, url_prefix='/api/books')

    return app
