from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from core.db import db
from core.schemas import PlainProjectSchema, ProjectSchema, ProjectUpdateSchema
from core.models import ProjectModel

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

        if project:
            project.name = project_data.get("name")
            project.description = project_data.get("description")
            project.budget = project_data.get("budget")
            project.is_active = project_data.get("is_active")
            project.project_type_id = project_data.get("project_type_id")
        else:
            project = ProjectModel(id=project_id, **project_data)

        try:
            db.session.add(project)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, message=str(e))

        return project

    @blp.response(
        202,
        description="Проект будет удален в мягкой форме, если будет найден и если не был уже удален.",
        example={"message": "проект удален(мягко)"}
    )
    @blp.alt_response(404, description="Проект не найден")
    @blp.alt_response(400, description="Данная ошибка возвращается, если у проекта есть не удаленные связи.")
    def delete(self, project_id):
        project = ProjectModel.query.get_or_404(project_id)
        name = project.name

        if project.is_deleted:
            abort(400,
                  message="Проект уже был удален. Обратитесь к администратору, если хоитете восстановить.")

        if not project.channels and not project.users:
            project.is_deleted = True
            try:
                db.session.add(project)
                db.session.commit()
            except SQLAlchemyError as e:
                abort(400, message=str(e))

            return {"message": f"Проект '{name}' удален(мягко)."}

        abort(400, message="Удалить проект не удалось. Убедитесь что нет активных связей.")

    @blp.response(200, ProjectSchema)
    def post(self, project_id):
        project = ProjectModel.query.get_or_404(project_id)

        if not project.is_deleted:
            abort(400, message="Проект и так не был удален.")

        project.is_deleted = False
        try:
            db.session.add(project)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, message=str(e))

        return project


@blp.route("/project/hard_delete/<int:project_id>")
class HardDeleteProject(MethodView):
    @blp.response(
        202,
        description="Проект будет удален безвозвратно, если будет найден и нет активных связей.",
        example={"message":"Проект был удален безвозвратно."}
    )
    def delete(self, project_id):
        project = ProjectModel.query.get_or_404(project_id)
        name = project.name

        try:
            db.session.delete(project)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, message=str(e))

        return {"message": f'Проект "{name}" удален безвозвратно.'}
