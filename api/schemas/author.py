from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema

from api.models.author import Author
from api.schemas.book import BookSchema
from api.utils.database import db


class AuthorSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Author
        sqla_session = db.session

    id = fields.Integer(dump_only=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    created = fields.String(dump_only=True)
    books = fields.Nested(BookSchema, many=True, only=["id", "title", "year"])
