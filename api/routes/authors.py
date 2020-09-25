import os
from werkzeug.utils import secure_filename
from flask import Blueprint, url_for, current_app
from flask import request
from flask_jwt_extended import jwt_required

from api.utils.responses import response_with
from api.utils import responses as resp
from api.models.author import Author
from api.schemas.author import AuthorSchema
from api.utils.database import db

author_routes = Blueprint("author_routes", __name__)

allowed_extensions = {'image/jpeg', 'image/png', 'jpeg'}


def allowed_file(filetype):
    return filetype in allowed_extensions


@author_routes.route("/", methods=["POST"])
@jwt_required
def create_author():
    try:
        data = request.get_json()
        author_schema = AuthorSchema()
        author = author_schema.load(data)
        result = author_schema.dump(author.create())
        return response_with(resp.SUCCESS_201, value={"author": result})
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


@author_routes.route("/", methods=["GET"])
def get_author_list():
    fetched = Author.query.all()
    author_schema = AuthorSchema(many=True, only=["first_name", "last_name", "id"])
    authors = author_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={"authors": authors})


@author_routes.route("/<int:author_id>", methods=["GET"])
def get_author_detail(author_id):
    fetched = Author.query.get_or_404(author_id)
    author_schema = AuthorSchema()
    author = author_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={"author": author})


@author_routes.route("/<int:author_id>", methods=["PUT"])
@jwt_required
def update_author_detail(author_id):
    data = request.get_json()
    get_author = Author.query.get_or_404(author_id)
    get_author.first_name = data["first_name"]
    get_author.last_name = data["last_name"]
    db.session.add(get_author)
    db.session.commit()
    author_schema = AuthorSchema()
    author = author_schema.dump(get_author)
    return response_with(resp.SUCCESS_200, value={"author": author})


@author_routes.route("/<int:author_id>", methods=["PATCH"])
@jwt_required
def modify_author_detail(author_id):
    data = request.get_json()
    get_author = Author.query.get(author_id)
    if data.get("first_name"):
        get_author.first_name = data["first_name"]
    if data.get("last_name"):
        get_author.last_name = data["last_name"]
    db.session.add(get_author)
    db.session.commit()
    author_schema = AuthorSchema()
    author = author_schema.dump(get_author)
    return response_with(resp.SUCCESS_200, value={"author": author})


@author_routes.route("/<int:author_id>", methods=["DELETE"])
@jwt_required
def delete_author(author_id):
    get_author = Author.query.get_or_404(author_id)
    db.session.delete(get_author)
    db.session.commit()
    return response_with(resp.SUCCESS_204)


@author_routes.route('/avatar/<int:author_id>', methods=['POST'])
# @jwt_required
def insert_author_avatar(author_id):
    try:
        file = request.files['avatar']
        get_author = Author.query.get_or_404(author_id)
        if file and allowed_file(file.content_type):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        get_author.avatar = url_for('uploaded_file', filename=filename, _external=True)
        db.session.add(get_author)
        db.session.commit()
        author_schema = AuthorSchema()
        author = author_schema.dump(get_author)
        return response_with(resp.SUCCESS_200, value={'author': author})
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)

