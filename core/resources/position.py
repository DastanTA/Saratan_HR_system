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
            abort(404, message="Данный проект был удален. Обратитесь к администратору.")

        return position
