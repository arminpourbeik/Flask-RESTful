import logging
import os

from flask import send_from_directory, jsonify

from api.models.author import Author
from api.models.book import Book
from api.models.user import User
from api.utils.database import db
from api.utils.responses import response_with
import api.utils.responses as resp
from main import create_app

from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.route('/avatar/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


SWAGGER_URL = '/api/docs'


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Book=Book, Author=Author)


@app.cli.command()
def add_admin():
    admin = User(
        username='admin',
        email='arminpourbeik@gmail.com',
        is_verified=True
    )
    admin.password = admin.generate_hash('admin')
    db.session.add(admin)
    db.session.commit()
    print('Admin user added.')


# START GLOBAL HTTP CONFIGURATIONS
@app.after_request
def add_header(response):
    return response


@app.errorhandler(400)
def bad_request(e):
    logging.error(e)
    return response_with(resp.BAD_REQUEST_400)


@app.errorhandler(500)
def server_error(e):
    logging.error(e)
    return response_with(resp.SERVER_ERROR_500)


@app.errorhandler(404)
def not_found(e):
    logging.error(e)
    return response_with(resp.SERVER_ERROR_404)


# END GLOBAL HTTP CONFIGURATIONS


@app.route('/api/spec')
def spec():
    swag = swagger(app, prefix='/api')
    swag['info']['base'] = 'http://localhost:5000'
    swag['info']['version'] = '1.0'
    swag['info']['title'] = 'Flask Author DB'
    return jsonify(swag)


swaggerui_blueprint = get_swaggerui_blueprint('/api/docs', '/api/spec', config={"app_name": "flask Author DB"})
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
