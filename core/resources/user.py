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

    @blp.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.query.filter(UserModel.is_deleted == False).all()


@blp.route("/user/<int:user_id>")
class GetUpdateSoftAndHardDeleteRecoverUser(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)

        if user.is_deleted:
            abort(400, message="Пользватель удален. Обратитесь к админу.")

        return user
