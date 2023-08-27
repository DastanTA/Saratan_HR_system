from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from core.db import db
from core.schemas import PlainOccupancySchema, OccupancySchema, OccupancyUpdateSchema
from core.models import OccupancyModel

blp = Blueprint("occupancies", __name__, description="Operations on occupancies")


@blp.route("/occupancy")
class GetAllAndCreateOccupancy(MethodView):
    @blp.arguments(PlainOccupancySchema)
    @blp.response(201, OccupancySchema)
    def post(self, occupancy_data):
        occupancy = OccupancyModel(**occupancy_data)

        try:
            db.session.add(occupancy)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, message=str(e))

        return occupancy

#     @blp.response(200, RoleSchema(many=True))
#     def get(self):
#         return RoleModel.query.filter(RoleModel.is_deleted == False).all()
#
#
# @blp.route("/role/<int:role_id>")
# class GetUpdateDeleteRecoverSingleRole(MethodView):
#     @blp.response(200, RoleSchema)
#     def get(self, role_id):
#         role = RoleModel.query.get_or_404(role_id)
#
#         if role.is_deleted:
#             abort(404, message="Данная роль была удалена. Обратитесь к администратору.")
#
#         return role
#
#     @blp.arguments(RoleUpdateSchema)
#     @blp.response(200, RoleSchema)
#     def put(self, role_data, role_id):
#         role = RoleModel.query.get_or_404(role_id)
#
#         if role.is_deleted:
#             abort(404, message="Данная роль была удалена. Обратитесь к администратору.")
#
#         if role:
#             role.name = role_data.get("name")
#             role.description = role_data.get("description")
#         else:
#             role = RoleModel(id=role_id, **role_data)
#
#         try:
#             db.session.add(role)
#             db.session.commit()
#         except SQLAlchemyError as e:
#             abort(400, message=str(e))
#
#         return role
#
#     @blp.response(
#         202,
#         description="Роль будет удалена в мягкой форме, если будет найдена и если не была уже удалена.",
#         example={"message": "Роль удалена(мягко)"}
#     )
#     @blp.alt_response(404, description="Роль не найдена")
#     def delete(self, role_id):
#         role = RoleModel.query.get_or_404(role_id)
#         name = role.name
#
#         if role.is_deleted:
#             abort(400,
#                   message="Данная Роль была уже удалена. Обратитесь к администратору, если хоитете восстановить.")
#
#         role.is_deleted = True
#         try:
#             db.session.add(role)
#             db.session.commit()
#         except SQLAlchemyError as e:
#             abort(400, message=str(e))
#
#         return {"message": f"Роль '{name}' удалена(мягко)."}
#
#     @blp.response(200, RoleSchema)
#     def post(self, role_id):
#         role = RoleModel.query.get_or_404(role_id)
#
#         if not role.is_deleted:
#             abort(400, message="Роль и так не былa удаленa.")
#
#         role.is_deleted = False
#         try:
#             db.session.add(role)
#             db.session.commit()
#         except SQLAlchemyError as e:
#             abort(400, message=str(e))
#
#         return role
#
#
# @blp.route("/role/hard_delete/<int:role_id>")
# class HardDeleteRole(MethodView):
#     @blp.response(
#         202,
#         description="Роль будет удалена безвозвратно, если будет найдена.",
#         example={"message": "Роль была удалена безвозвратно."}
#     )
#     def delete(self, role_id):
#         role = RoleModel.query.get_or_404(role_id)
#         name = role.name
#
#         try:
#             db.session.delete(role)
#             db.session.commit()
#         except SQLAlchemyError as e:
#             abort(400, message=str(e))
#
#         return {"message": f'Роль "{name}" удалена безвозвратно.'}
