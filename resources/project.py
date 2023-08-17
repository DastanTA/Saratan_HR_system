from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from schemas import PlainProjectSchema, ProjectSchema
from models import ProjectModel


blp = Blueprint("projects", __name__, description="Operations on projects")


@blp.route("/project")
class GetAllAndCreateProject(MethodView):
    @blp.arguments(PlainProjectSchema)
    @blp.response(201, ProjectSchema)
    def post(self, project_data):
        project = ProjectModel(**project_data)

        try:
            db.session.add(project)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, message=str(e))

        return project
