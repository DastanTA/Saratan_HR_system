from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from core.db import db
from core.schemas import PlainUserSchema, UserSchema, UserUpdateSchema
from core.models import UserModel

blp = Blueprint("users", __name__, description="Operations on users")


@blp.route("/user")
class GetAllAndCreateUser(MethodView):
    @blp.arguments(PlainUserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        user = UserModel(**user_data)

        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, message=str(e))

        return user
