from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from core.db import db
from config import Config

from core.resources.project_type import blp as ProjectTypeBlueprint
from core.resources.project import blp as ProjectBlueprint
from core.resources.channel import blp as ChannelBlueprint
from core.resources.position import blp as PositionBlueprint
from core.resources.role import blp as RoleBlueprint
from core.resources.occupancy import blp as OccupancyBlueprint
from core.resources.user import blp as UserBlueprint

from core.models import UserModel, BlocklistModel


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)

    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        if BlocklistModel.query.filter(BlocklistModel.jti == jwt_payload["jti"]).first():
            return True
        return False

    @jwt.revoked_token_loader
    def revoked_taken_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked/Токен был отозван.", "error": "token_revoked"}
            ),
            401,
        )

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        user = UserModel.query.get_or_404(identity)

        return {"role": user.role.name}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired/Срок жизни токена истек.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed/Не удалось верифицировать токен.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token/В запросе нет токена.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    api.register_blueprint(ProjectTypeBlueprint)
    api.register_blueprint(ProjectBlueprint)
    api.register_blueprint(ChannelBlueprint)
    api.register_blueprint(PositionBlueprint)
    api.register_blueprint(RoleBlueprint)
    api.register_blueprint(OccupancyBlueprint)
    api.register_blueprint(UserBlueprint)

    return app
