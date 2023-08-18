from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from schemas import PlainProjectSchema, ProjectSchema, ProjectUpdateSchema
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

    @blp.response(200, ProjectSchema(many=True))
    def get(self):
        return ProjectModel.query.filter(ProjectModel.is_deleted == False).all()


@blp.route("/project/<int:project_id>")
class GetUpdateDeleteRecoverSingleProject(MethodView):
    @blp.response(200, ProjectSchema)
    def get(self, project_id):
        project = ProjectModel.query.get_or_404(project_id)

        if project.is_deleted:
            abort(404, message="Данный проект был удален. Обратитесь к администратору.")

        return project

    @blp.arguments(ProjectUpdateSchema)
    @blp.response(200, ProjectSchema)
    def put(self, project_data, project_id):
        project = ProjectModel.query.get_or_404(project_id)

        if project.is_deleted:
            abort(404, message="Данный проект был удален. Обратитесь к администратору.")

        if project_data.get("name"):
            project.name = project_data.get("name")
        if project_data.get("description"):
            project.description = project_data.get("description")
        if project_data.get("budget"):
            project.budget = project_data.get("budget")
        if "is_active" in project_data:
            project.is_active = project_data.get("is_active")

        try:
            db.session.add(project)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, message=str(e))

        return project
