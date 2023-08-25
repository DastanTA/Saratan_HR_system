from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from core.db import db
from core.schemas import PlainChannelSchema, ChannelSchema, ChannelUpdateSchema
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

    @blp.arguments(ChannelUpdateSchema)
    @blp.response(200, ChannelSchema)
    def put(self, channel_data, channel_id):
        channel = ChannelModel.query.get_or_404(channel_id)

        if channel.is_deleted:
            abort(404, message="Данный канал был удален. Обратитесь к администратору.")

        if channel:
            channel.is_original = channel_data.get("is_original")
            channel.channel_name = channel_data.get("channel_name")
            channel.description = channel_data.get("description")
            channel.url_address = channel_data.get("url_address")
            channel.is_active = channel_data.get("is_active")
            channel.manager_id = channel_data.get("manager_id")
            channel.project_id = channel_data.get("project_id")
        else:
            channel = ChannelModel(id=channel_id, **channel_data)

        try:
            db.session.add(channel)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, message=str(e))

        return channel

    @blp.response(
        202,
        description="Канал будет удален в мягкой форме, если будет найден и если не был уже удален.",
        example={"message": "проект удален(мягко)"}
    )
    @blp.alt_response(404, description="Канал не найден")
    def delete(self, channel_id):
        channel = ChannelModel.query.get_or_404(channel_id)
        name = channel.channel_name

        if channel.is_deleted:
            abort(400,
                  message="Канал уже был удален. Обратитесь к администратору, если хоитете восстановить.")

        channel.is_deleted = True
        try:
            db.session.add(channel)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, message=str(e))

        return {"message": f"Канал '{name}' удален(мягко)."}

    @blp.response(200, ChannelSchema)
    def post(self, channel_id):
        channel = ChannelModel.query.get_or_404(channel_id)

        if not channel.is_deleted:
            abort(400, message="Проект и так не был удален.")

        channel.is_deleted = False
        try:
            db.session.add(channel)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, message=str(e))

        return channel
