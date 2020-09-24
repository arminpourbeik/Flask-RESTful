from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema

from api.models.book import Book
from api.utils.database import db


class BookSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Book
        sqla_session = db.session

    id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    year = fields.Integer(required=True)
    author_id = fields.Integer()
