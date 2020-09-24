from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema

from api.models.user import User
from api.utils.database import db


class UserSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = User
        sqla_session = db.session

    id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
