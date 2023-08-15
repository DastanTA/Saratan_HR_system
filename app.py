import os
from datetime import timedelta

from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv

from db import db

from resources.project_type import blp as ProjectTypeBlueprint

from models import UserModel


def create_app(db_url=None):
    app = Flask(__name__)
    load_dotenv()

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Saratan HRS REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or (f"postgresql://{os.getenv('DB_USERNAME')}:"
                                                       f"{os.getenv('DB_PASSWORD')}@localhost/{os.getenv('DB_NAME')}")
    # app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "postgresql:///hrs_db")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)

    app.config["JWT_SECRET_KEY"] = "Saratan_HRS"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
    jwt = JWTManager(app)

    # @jwt.token_in_blocklist_loader
    # def check_if_token_in_blocklist(jwt_header, jwt_payload):
    #     if BlockListModel.query.filter(BlockListModel.jti == jwt_payload["jti"]).first():
    #         return True
    #     return False
    #
    # @jwt.revoked_token_loader
    # def revoked_taken_callback(jwt_header, jwt_payload):
    #     return (
    #         jsonify(
    #             {"description": "The token has been revoked/Токен был отозван.", "error": "token_revoked"}
    #         ),
    #         401,
    #     )
    #
    # @jwt.additional_claims_loader
    # def add_claims_to_jwt(identity):
    #     user = UserModel.query.get_or_404(identity)
    #
    #     return {"role": user.role.name}
    #
    # @jwt.expired_token_loader
    # def expired_token_callback(jwt_header, jwt_payload):
    #     return (
    #         jsonify({"message": "The token has expired/Срок жизни токена истек.", "error": "token_expired"}),
    #         401,
    #     )
    #
    # @jwt.invalid_token_loader
    # def invalid_token_callback(error):
    #     return (
    #         jsonify(
    #             {"message": "Signature verification failed/Не удалось верифицировать токен.", "error": "invalid_token"}
    #         ),
    #         401,
    #     )
    #
    # @jwt.unauthorized_loader
    # def missing_token_callback(error):
    #     return (
    #         jsonify(
    #             {
    #                 "description": "Request does not contain an access token/В запросе нет токена.",
    #                 "error": "authorization_required",
    #             }
    #         ),
    #         401,
    #     )

    api.register_blueprint(ProjectTypeBlueprint)

    return app
