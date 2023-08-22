from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from core.db import db
from core.schemas import PlainChannelSchema, ChannelSchema
from core.models import ChannelModel

blp = Blueprint("channels", __name__, description="Operations on channels")


@blp.route("/channel")
class GetAllAndCreateProject(MethodView):
    @blp.arguments(PlainChannelSchema)
    @blp.response(201, ChannelSchema)
    def post(self, channel_data):
        channel = ChannelModel(**channel_data)

        try:
            db.session.add(channel)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, message=str(e))

        return channel
