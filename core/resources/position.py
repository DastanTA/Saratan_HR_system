from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from core.db import db
from core.schemas import PlainPositionSchema, PositionSchema, PositionUpdateSchema
from core.models import PositionModel

blp = Blueprint("positions", __name__, description="Operations on positions")


@blp.route("/position")
class GetAllAndCreatePosition(MethodView):
    @blp.arguments(PlainPositionSchema)
    @blp.response(201, PositionSchema)
    def post(self, position_data):
        position = PositionModel(**position_data)

        try:
            db.session.add(position)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, message=str(e))

        return position

    @blp.response(200, PositionSchema(many=True))
    def get(self):
        return PositionModel.query.filter(PositionModel.is_deleted == False).all()


@blp.route("/position/<int:position_id>")
class GetUpdateDeleteRecoverSinglePosition(MethodView):
    @blp.response(200, PositionSchema)
    def get(self, position_id):
        position = PositionModel.query.get_or_404(position_id)

        if position.is_deleted:
            abort(404, message="Данная позиция была удалена. Обратитесь к администратору.")

        return position

    @blp.arguments(PositionUpdateSchema)
    @blp.response(200, PositionSchema)
    def put(self, position_data, position_id):
        position = PositionModel.query.get_or_404(position_id)

        if position.is_deleted:
            abort(404, message="Данная позиция была удалена. Обратитесь к администратору.")

        if position:
            position.name = position_data.get("name")
            position.description = position_data.get("description")
        else:
            position = PositionModel(id=position_id, **position_data)

        try:
            db.session.add(position)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, message=str(e))

        return position

    @blp.response(
        202,
        description="Позиция будет удалена в мягкой форме, если будет найдена и если не была уже удалена.",
        example={"message": "Позиция удалена(мягко)"}
    )
    @blp.alt_response(404, description="Позиция не найдена")
    def delete(self, position_id):
        position = PositionModel.query.get_or_404(position_id)
        name = position.name

        if position.is_deleted:
            abort(400,
                  message="Данная позиция была уже удалена. Обратитесь к администратору, если хоитете восстановить.")

        position.is_deleted = True
        try:
            db.session.add(position)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, message=str(e))

        return {"message": f"Позиция '{name}' удалена(мягко)."}

    @blp.response(200, PositionSchema)
    def post(self, position_id):
        position = PositionModel.query.get_or_404(position_id)

        if not position.is_deleted:
            abort(400, message="Позиция и так не был удален.")

        position.is_deleted = False
        try:
            db.session.add(position)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, message=str(e))

        return position
