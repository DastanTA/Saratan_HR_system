from marshmallow import Schema, fields

from user_schemas import PlainUserSchema
from project_schemas import PlainProjectSchema


class PlainChannelSchema(Schema):
    id = fields.Int(dump_only=True)
    is_original = fields.Boolean(required=True)
    channel_name = fields.Str(required=True)
    description = fields.Str(required=False)
    url_address = fields.Str(required=True)
    is_active = fields.Boolean(required=True, default=True)
    # manager_id = fields.Int(required=True)
    # project_id = fields.Int(required=True)


class ChannelSchema(PlainChannelSchema):
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    manager = fields.Nested(PlainUserSchema(), dump_only=True)
    project = fields.Nested(PlainProjectSchema(), dump_only=True)
