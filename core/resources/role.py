from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt

from core.db import db
from core.schemas import PlainRoleSchema, RoleSchema, RoleUpdateSchema
from core.models import RoleModel, UserModel

blp = Blueprint("roles", __name__, description="Operations on roles")


@blp.route("/role")
class GetAllAndCreateRole(MethodView):
    @jwt_required()
    @blp.arguments(PlainRoleSchema)
    @blp.response(201, RoleSchema)
    def post(self, role_data):
        access_list = ["Owner", "admin"]
        users_role = get_jwt().get("role")

        if users_role not in access_list:
            abort(403, message="У вас нет доступа для создания роли.")

        role = RoleModel(**role_data)

        try:
            db.session.add(role)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, message=str(e))

        return role

    @jwt_required()
    @blp.response(200, RoleSchema(many=True))
    def get(self):
        access_list = ["Owner", "admin", "HR", "Project Manager", "Project Manager Assistant"]
        users_role = get_jwt().get("role")

        if users_role not in access_list:
            abort(403, message="У вас нет доступа для просмотра всех ролей.")

        return RoleModel.query.filter(RoleModel.is_deleted == False).all()


@blp.route("/role/<int:role_id>")
class GetUpdateDeleteRecoverSingleRole(MethodView):
    @jwt_required()
    @blp.response(200, RoleSchema)
    def get(self, role_id):
        access_list = ["Owner", "admin", "HR", "Project Manager", "Project Manager Assistant"]
        users_role = get_jwt().get("role")
        role = RoleModel.query.get_or_404(role_id)

        if users_role in access_list or users_role == role.name:
            if role.is_deleted:
                abort(404, message="Данная роль была удалена. Обратитесь к администратору.")
            return role
        else:
            abort(403, message=f"У вас нет доступа для просмотра роли.")

    @jwt_required()
    @blp.arguments(RoleUpdateSchema)
    @blp.response(200, RoleSchema)
    def put(self, role_data, role_id):
        access_list = ["Owner", "admin"]
        users_role = get_jwt().get("role")

        if users_role not in access_list:
            abort(403, message="У вас нет доступа для редактирования роли.")

        role = RoleModel.query.get_or_404(role_id)

        if role.is_deleted:
            abort(404, message="Данная роль была удалена. Обратитесь к администратору.")

        if role:
            role.name = role_data.get("name")
            role.description = role_data.get("description")
        else:
            role = RoleModel(id=role_id, **role_data)

        try:
            db.session.add(role)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, message=str(e))

        return role

    @jwt_required()
    @blp.response(
        202,
        description="Роль будет удалена в мягкой форме, если будет найдена и если не была уже удалена.",
        example={"message": "Роль удалена(мягко)"}
    )
    @blp.alt_response(404, description="Роль не найдена")
    def delete(self, role_id):
        access_list = ["Owner", "admin"]
        users_role = get_jwt().get("role")

        if users_role not in access_list:
            abort(403, message="У вас нет доступа для удаления роли.")

        role = RoleModel.query.get_or_404(role_id)
        name = role.name

        if role.is_deleted:
            abort(400,
                  message="Данная Роль была уже удалена. Обратитесь к администратору, если хоитете восстановить.")

        role.is_deleted = True
        try:
            db.session.add(role)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, message=str(e))

        return {"message": f"Роль '{name}' удалена(мягко)."}

    @jwt_required()
    @blp.response(200, RoleSchema)
    def post(self, role_id):
        access_list = ["Owner", "admin"]
        users_role = get_jwt().get("role")

        if users_role not in access_list:
            abort(403, message="У вас нет доступа для восстановления роли.")

        role = RoleModel.query.get_or_404(role_id)

        if not role.is_deleted:
            abort(400, message="Роль и так не былa удаленa.")

        role.is_deleted = False
        try:
            db.session.add(role)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, message=str(e))

        return role


@blp.route("/role/hard_delete/<int:role_id>")
class HardDeleteRole(MethodView):
    @jwt_required()
    @blp.response(
        202,
        description="Роль будет удалена безвозвратно, если будет найдена.",
        example={"message": "Роль была удалена безвозвратно."}
    )
    def delete(self, role_id):
        access_list = ["Owner", "admin"]
        users_role = get_jwt().get("role")

        if users_role not in access_list:
            abort(403, message="У вас нет доступа для безвозвратного удаления роли из базы.")

        role = RoleModel.query.get_or_404(role_id)
        name = role.name

        try:
            db.session.delete(role)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, message=str(e))

        return {"message": f'Роль "{name}" удалена безвозвратно.'}
