import os
from datetime import timedelta

from dotenv import load_dotenv


class Config:
    load_dotenv()

    PROPAGATE_EXCEPTIONS = True
    API_TITLE = "Saratan HRS REST API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    #SQLALCHEMY_DATABASE_URI = (f"postgresql://{os.getenv('DB_USERNAME')}:"
    #                           f"{os.getenv('DB_PASSWORD')}@localhost/{os.getenv('DB_NAME')}")
    #SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql:///hrs_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "Saratan_HRS"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
