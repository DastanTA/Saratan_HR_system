from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from core.db import db
from core.schemas import PlainChannelSchema
from core.models import ChannelModel

blp = Blueprint("channels", __name__, description="Operations on channels")


@blp.route("/project")
class GetAllAndCreateProject(MethodView):
    pass