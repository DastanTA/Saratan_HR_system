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

    @blp.response(200, ChannelSchema(many=True))
    def get(self):
        return ChannelModel.query.filter(ChannelModel.is_deleted == False).all()


@blp.route("/channel/<int:channel_id>")
class GetUpdateDeleteRecoverChannel(MethodView):
    @blp.response(200, ChannelSchema)
    def get(self, channel_id):
        channel = ChannelModel.query.filter(ChannelModel.id == channel_id).first()

        if channel.is_deleted:
            abort(400, message="Канал был удален. Обратитесь к админу, если хотите восстановить.")

        return channel
