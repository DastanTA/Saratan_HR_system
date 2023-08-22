from marshmallow import Schema, fields


class PlainChannelSchema(Schema):
    id = fields.Int(dump_only=True)
    is_original = fields.Boolean(default=True)
    channel_name = fields.Str(required=True)
    description = fields.Str(required=False)
    url_address = fields.Str(required=True)
    is_active = fields.Boolean(default=True)
