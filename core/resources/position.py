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
