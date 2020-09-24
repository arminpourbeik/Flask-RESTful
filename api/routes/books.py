from flask import Blueprint
from flask import request
from api.utils.responses import response_with
from api.utils import responses as resp

from api.models.book import Book
from api.schemas.book import BookSchema
from api.utils.database import db


book_routes = Blueprint("book_routes", __name__)


@book_routes.route("/", methods=["POST"])
def create_book():
    try:
        data = request.get_json()
        book_schema = BookSchema()
        book = book_schema.load(data)
        result = book_schema.dump(book.create())
        return response_with(resp.SUCCESS_201, value={"book": result})
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


@book_routes.route("/", methods=["GET"])
def get_book_list():
    fetched = Book.query.all()
    book_schema = BookSchema(many=True, only=["title", "year", "author_id"])
    books = book_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={"books": books})


@book_routes.route("/<int:book_id>", methods=["GET"])
def get_book_detail(book_id):
    fetched = Book.query.get_or_404(book_id)
    book_schema = BookSchema()
    book = book_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={"book": book})


@book_routes.route("/<int:book_id>", methods=["PUT"])
def update_book_detail(book_id):
    data = request.get_json()
    get_book = Book.query.get_or_404(book_id)
    get_book.title = data["title"]
    get_book.year = data["year"]
    db.session.add(get_book)
    db.session.commit()
    book_schema = BookSchema()
    book = book_schema.dump(get_book)

    return response_with(resp.SUCCESS_200, value={"book": book})


@book_routes.route("/<int:book_id>", methods=["PATCH"])
def modify_book_detail(book_id):
    data = request.get_json()
    get_book = Book.query.get_or_404(book_id)
    if data.get("title"):
        get_book.title = data["title"]
    if data.get("year"):
        get_book.year = data["year"]
    db.session.add(get_book)
    db.session.commit()
    book_schema = BookSchema()
    book = book_schema.dump(get_book)

    return response_with(resp.SUCCESS_200, value={"book": book})


@book_routes.route("/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    get_book = Book.query.get_or_404(book_id)
    db.session.delete(get_book)
    db.session.commit()

    return response_with(resp.SUCCESS_204)
