from marshmallow import Schema, fields


class PlainChannelSchema(Schema):
    id = fields.Int(dump_only=True)
    is_original = fields.Boolean(required=True)
    channel_name = fields.Str(required=True)
    description = fields.Str(required=False)
    url_address = fields.Str(required=True)
    is_active = fields.Boolean(required=True, default=True)
    # manager_id = fields.Int(required=True)
    # project_id = fields.Int(required=True)


class PlainProjectTypeSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=False)


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


class PlainProjectSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=False)
    budget = fields.Int(required=False)
    is_active = fields.Boolean(required=False, default=True)
    project_type_id = fields.Int(required=False)


class PlainPositionSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=False)


class PlainRoleSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=False)


class PlainOccupancySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=False)


class OccupancySchema(PlainOccupancySchema):
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    users = fields.List(fields.Nested(PlainUserSchema()), dump_only=True)


class RoleSchema(PlainRoleSchema):
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    users = fields.List(fields.Nested(PlainUserSchema()), dump_only=True)


class PositionSchema(PlainPositionSchema):
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    users = fields.List(fields.Nested(PlainUserSchema()), dump_only=True)


class ProjectTypeSchema(PlainProjectTypeSchema):
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    projects = fields.List(fields.Nested(PlainProjectTypeSchema()), dump_only=True)


class ProjectSchema(PlainProjectSchema):
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    users = fields.List(fields.Nested(PlainUserSchema()), dump_only=True)
    project_type_id = fields.Int(Load_only=True)
    project_type = fields.Nested(PlainProjectTypeSchema(), dump_only=True)
    channels = fields.List(fields.Nested(PlainChannelSchema()), dump_only=True)


class ChannelSchema(PlainChannelSchema):
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    manager = fields.Nested(PlainUserSchema(), dump_only=True)
    project = fields.Nested(PlainProjectSchema(), dump_only=True)


class UserSchema(PlainUserSchema):
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    is_active = fields.Boolean(dump_only=True)
    role_id = fields.Int(load_only=True)
    role = fields.Nested(PlainRoleSchema(), dump_only=True)
    occupancy_id = fields.Int(load_only=True)
    occupancy = fields.Nested(PlainOccupancySchema(), dump_only=True)
    positions = fields.List(fields.Nested(PlainPositionSchema()), dump_only=True)
    projects = fields.List(fields.Nested(PlainProjectSchema()), dump_only=True)
    channels = fields.List(fields.Nested(PlainChannelSchema()), dump_only=True)


class ProjectTypeUpdateSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=False)


class ProjectUpdateSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=False)
    budget = fields.Int(required=False)
    is_active = fields.Boolean(required=True)
    project_type_id = fields.Int(required=False)


class ChannelUpdateSchema(Schema):
    is_original = fields.Boolean(required=True)
    channel_name = fields.Str(required=True)
    description = fields.Str(required=False)
    url_address = fields.Str(required=True)
    is_active = fields.Boolean(required=True, default=True)
    manager_id = fields.Int(required=False)
    project_id = fields.Int(required=False)


class PositionUpdateSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=False)


class RoleUpdateSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=False)


class OccupancyUpdateSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=False)


class UserUpdateSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)
    phone = fields.Str(required=False)
    first_name = fields.Str(required=True)
    middle_name = fields.Str(required=False)
    last_name = fields.Str(required=True)
    basic_profession = fields.Str(required=True)
    notes = fields.Str(required=False)
    is_active = fields.Boolean(required=True)
