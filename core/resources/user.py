from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token

from core.db import db
from core.schemas import PlainUserSchema, UserSchema, UserUpdateSchema, UserLoginSchema
from core.models import UserModel

blp = Blueprint("users", __name__, description="Operations on users")


@blp.route("/user")
class GetAllAndCreateUser(MethodView):
    @blp.arguments(PlainUserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        user = UserModel(
            username=user_data.get("username"),
            email=user_data.get("email"),
            password=pbkdf2_sha256.hash(user_data.get("password")),
            phone=user_data.get("phone"),
            first_name=user_data.get("first_name"),
            middle_name=user_data.get("middle_name"),
            last_name=user_data.get("last_name"),
            basic_profession=user_data.get("basic_profession"),
            notes=user_data.get("notes")
        )

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

    @blp.arguments(UserUpdateSchema)
    @blp.response(200, UserSchema)
    def put(self, user_data, user_id):
        user = UserModel.query.get_or_404(user_id)

        if user.is_deleted:
            abort(400, message="Пользватель удален. Обратитесь к админу.")

        if user:
            user.username = user_data.get("username"),
            user.email = user_data.get("email"),
            user.phone = user_data.get("phone"),
            user.first_name = user_data.get("first_name"),
            user.middle_name = user_data.get("middle_name"),
            user.last_name = user_data.get("last_name"),
            user.basic_profession = user_data.get("basic_profession"),
            user.notes = user_data.get("notes")
            user.is_active = user_data.get("is_active")
        else:
            abort(400, message=f"Пользователя с id номером: '{user_id}' не существует в базе.")

        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, message=str(e))

        return user

    @blp.response(
        202,
        description="Пользователь будет удален в мягкой форме, если будет найден и если не была уже удален.",
        example={"message": "Пользователь удален(мягко)"}
    )
    @blp.alt_response(404, description="Пользователь не найден")
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)

        if user.is_deleted:
            abort(400,
                  message="Данный пользователь был уже удален. Обратитесь к администратору, если хоитете восстановить.")

        user.is_deleted = True
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, message=str(e))

        return {"message": f"Пользователь '{user.username}' удален(мягко)."}

    @blp.response(200, UserSchema)
    def post(self, user_id):
        user = UserModel.query.get_or_404(user_id)

        if not user.is_deleted:
            abort(400, message="Пользователь и так не был удален.")

        user.is_deleted = False
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, message=str(e))

        return user


@blp.route("/user/hard_delete/<int:user_id>")
class HardDeleteUser(MethodView):
    @blp.response(
        202,
        description="Пользователь будет удален безвозвратно, если будет найден.",
        example={"message": "Пользователь был удален безвозвратно."}
    )
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)

        try:
            db.session.delete(user)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, message=str(e))

        return {"message": f'Пользователь "{user.username}" удален безвозвратно.'}


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserLoginSchema)
    def post(self, user_login_data):
        user = UserModel.query.filter(UserModel.username == user_login_data["username"]).first()

        if user and pbkdf2_sha256.verify(user_login_data["password"], user.password):
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token}, 200

        abort(401, message="Неправильный логин или пароль.")
