from marshmallow import Schema, fields

from project_type_schemas import PlainProjectTypeSchema
from user_schemas import PlainUserSchema
from channel_schemas import PlainChannelSchema


class PlainProjectSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=False)
    budget = fields.Int(required=False)
    is_active = fields.Boolean(required=False, default=True)
    project_type_id = fields.Int(required=False)


class ProjectSchema(PlainProjectSchema):
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    users = fields.List(fields.Nested(PlainUserSchema()), dump_only=True)
    project_type_id = fields.Int(Load_only=True)
    project_type = fields.Nested(PlainProjectTypeSchema(), dump_only=True)
    channels = fields.List(fields.Nested(PlainChannelSchema()), dump_only=True)


class ProjectUpdateSchema(Schema):
    name = fields.Str(required=False)
    description = fields.Str(required=False)
    budget = fields.Int(required=False)
    is_active = fields.Boolean(required=False)
    project_type_id = fields.Int(required=False)