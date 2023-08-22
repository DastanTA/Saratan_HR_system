from marshmallow import Schema, fields


class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=False)
    email = fields.Str(required=True)
    password = fields.Str(required=True)
    phone = fields.Str(required=False)
    first_name = fields.Str(required=True)
    middle_name = fields.Str(required=False)
    last_name = fields.Str(required=True)
    basic_profession = fields.Str(required=True)
    notes = fields.Str(required=False)
