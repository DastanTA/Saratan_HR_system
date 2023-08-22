from marshmallow import Schema, fields


class PlainProjectTypeSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=False)


class ProjectTypeSchema(PlainProjectTypeSchema):
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    projects = fields.List(fields.Nested(PlainProjectTypeSchema()), dump_only=True)


class ProjectTypeUpdateSchema(Schema):
    name = fields.Str(required=False)
    description = fields.Str(required=False)
