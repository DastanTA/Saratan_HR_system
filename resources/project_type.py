from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from schemas import PlainProjectTypeSchema, ProjectTypeSchema
from models import ProjectTypeModel


blp = Blueprint("project_types", __name__, description="Operations on project_types")


@blp.route("/project_type")
class CreateAndAllProjectType(MethodView):
    @blp.arguments(PlainProjectTypeSchema)
    @blp.response(201, PlainProjectTypeSchema)
    def post(self, project_type_data):
        project_type = ProjectTypeModel(
            name=project_type_data["name"],
            description=project_type_data["description"]
        )
        try:
            db.session.add(project_type)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A project_type with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the new project_type.")
        return project_type, 201

    @blp.response(200, ProjectTypeSchema(many=True))
    def get(self):
        return ProjectTypeModel.query.filter(ProjectTypeModel.is_deleted == False).all()
