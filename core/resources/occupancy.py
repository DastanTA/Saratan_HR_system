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

    @blp.response(200, OccupancySchema(many=True))
    def get(self):
        return OccupancyModel.query.filter(OccupancyModel.is_deleted == False).all()


@blp.route("/occupancy/<int:occupancy_id>")
class GetUpdateDeleteRecoverSingleOccupancy(MethodView):
    @blp.response(200, OccupancySchema)
    def get(self, occupancy_id):
        occupancy = OccupancyModel.query.get_or_404(occupancy_id)

        if occupancy.is_deleted:
            abort(404, message="Данный вид размещения был удален. Обратитесь к администратору.")

        return occupancy

    @blp.arguments(OccupancyUpdateSchema)
    @blp.response(200, OccupancySchema)
    def put(self, occupancy_data, occupancy_id):
        occupancy = OccupancyModel.query.get_or_404(occupancy_id)

        if occupancy.is_deleted:
            abort(404, message="Данный вид размещения был удален. Обратитесь к администратору.")

        if occupancy:
            occupancy.name = occupancy_data.get("name")
            occupancy.description = occupancy_data.get("description")
        else:
            occupancy = OccupancyModel(id=occupancy_id, **occupancy_data)

        try:
            db.session.add(occupancy)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, message=str(e))

        return occupancy

    @blp.response(
        202,
        description="Вид размещения будет удален в мягкой форме, если будет найден и если не был уже удален.",
        example={"message": "Вид размещения удален(мягко)"}
    )
    @blp.alt_response(404, description="Вид размещения не найден.")
    def delete(self, occupancy_id):
        occupancy = OccupancyModel.query.get_or_404(occupancy_id)
        name = occupancy.name

        if occupancy.is_deleted:
            abort(400,
                  message="Данный вид размещения был уже удален. Обратитесь к администратору, если хоитете восстановить.")

        occupancy.is_deleted = True
        try:
            db.session.add(occupancy)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, message=str(e))

        return {"message": f"Вид размещения '{name}' удален(мягко)."}

    @blp.response(200, OccupancySchema)
    def post(self, occupancy_id):
        occupancy = OccupancyModel.query.get_or_404(occupancy_id)

        if not occupancy.is_deleted:
            abort(400, message="Вид размещения и так не был удален.")

        occupancy.is_deleted = False
        try:
            db.session.add(occupancy)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, message=str(e))

        return occupancy


@blp.route("/occupancy/hard_delete/<int:occupancy_id>")
class HardDeleteOccupancy(MethodView):
    @blp.response(
        202,
        description="Вид размещения будет удален безвозвратно, если будет найдена.",
        example={"message": "Вид размещения был удален безвозвратно."}
    )
    def delete(self, occupancy_id):
        occupancy = OccupancyModel.query.get_or_404(occupancy_id)
        name = occupancy.name

        try:
            db.session.delete(occupancy)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, message=str(e))

        return {"message": f'Вид размещения "{name}" удален безвозвратно.'}
