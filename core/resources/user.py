from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity

from core.db import db
from core.schemas import PlainUserSchema, UserSchema, UserUpdateSchema, UserLoginSchema
from core.models import UserModel, BlocklistModel

blp = Blueprint("users", __name__, description="Operations on users")


@blp.route("/user")
class GetAllAndCreateUser(MethodView):
    @jwt_required()
    @blp.arguments(PlainUserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        jwt = get_jwt()
        role = jwt.get("role")
        access_list = ["HR", "Owner", "admin"]

        if role not in access_list:
            abort(403, message="У вас нет доступа для регистрации нового пользователя.")

        user = UserModel(
            username=user_data.get("username"),
            email=user_data.get("email"),
            password=pbkdf2_sha256.hash(user_data.get("password")),
            phone=user_data.get("phone"),
            first_name=user_data.get("first_name"),
            middle_name=user_data.get("middle_name"),
            last_name=user_data.get("last_name"),
            basic_profession=user_data.get("basic_profession"),
            notes=user_data.get("notes"),
            role_id=user_data.get("role_id")
        )

        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, message=str(e))

        return user

    @jwt_required()
    @blp.response(200, UserSchema(many=True))
    def get(self):
        jwt = get_jwt()
        role = jwt.get("role")
        access_list = ["HR", "Owner", "admin", "Project Manager", "Project Manager Assistant"]

        if role not in access_list:
            abort(403, message="У вас нет доступа для просмотра всех пользователей.")

        return UserModel.query.filter(UserModel.is_deleted == False).all()


@blp.route("/user/<int:user_id>")
class GetUpdateSoftAndHardDeleteRecoverUser(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema)
    def get(self, user_id):
        jwt = get_jwt()
        role = jwt.get("role")
        access_list = ["HR", "Owner", "admin", "Project Manager", "Project Manager Assistant"]
        accessing_user_id = get_jwt_identity()

        if role in access_list or accessing_user_id == user_id:
            user = UserModel.query.get_or_404(user_id)
            if user.is_deleted:
                abort(400, message="Пользватель удален. Обратитесь к админу.")
        else:
            abort(403, message="У вас нет доступа для просмотра данного пользователя.")

        return user

    @jwt_required()
    @blp.arguments(UserUpdateSchema)
    @blp.response(200, UserSchema)
    def put(self, user_data, user_id):
        jwt = get_jwt()
        role = jwt.get("role")
        access_list = ["HR", "Owner", "admin", "Project Manager", "Project Manager Assistant"]

        if role not in access_list:
            abort(403, message="У вас нет доступа для редактирования данных пользователей.")

        user = UserModel.query.get_or_404(user_id)

        if user.is_deleted:
            abort(400, message="Пользватель удален. Обратитесь к админу/HR.")

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
            user.role_id = user_data.get("role_id")
        else:
            abort(400, message=f"Пользователя с id номером: '{user_id}' не существует в базе.")

        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, message=str(e))

        return user

    @jwt_required()
    @blp.response(
        202,
        description="Пользователь будет удален в мягкой форме, если будет найден и если не была уже удален.",
        example={"message": "Пользователь удален(мягко)"}
    )
    @blp.alt_response(404, description="Пользователь не найден")
    def delete(self, user_id):
        access_list = ["HR", "Owner", "admin"]
        role = get_jwt().get("role")

        if role not in access_list:
            abort(403, message="У вас нет доступа для удаления пользователей.")

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

    @jwt_required()
    @blp.response(200, UserSchema)
    def post(self, user_id):
        access_list = ["HR", "Owner", "admin"]
        role = get_jwt().get("role")

        if role not in access_list:
            abort(403, message="У вас нет доступа для восстановления пользователей.")

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
    @jwt_required()
    @blp.response(
        202,
        description="Пользователь будет удален безвозвратно, если будет найден.",
        example={"message": "Пользователь был удален безвозвратно."}
    )
    def delete(self, user_id):
        access_list = ["Owner", "admin"]
        role = get_jwt().get("role")

        if role not in access_list:
            abort(403, message="У вас нет доступа для безвозвратного удаления пользователей из базы!")

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


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        new_blocked_jti = BlocklistModel(jti=jti)

        try:
            db.session.add(new_blocked_jti)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return {"message": "Вы вышли из учетной записи. / Successfully logged out."}
