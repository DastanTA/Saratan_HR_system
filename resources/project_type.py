from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from schemas import PlainProjectTypeSchema, ProjectTypeSchema, ProjectTypeUpdateSchema
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


@blp.route("/project_type/<int:project_type_id>")
class CreateAndAllProjectType(MethodView):
    @blp.response(200, ProjectTypeSchema)
    def get(self, project_type_id):
        project_type = ProjectTypeModel.query.get_or_404(project_type_id)
        if project_type.is_deleted:
            abort(400, message="Этот тип проекта был удален. Обратитесь к суперадмину за деталями.")
        return project_type

    @blp.arguments(ProjectTypeUpdateSchema)
    @blp.response(200, ProjectTypeSchema)
    def put(self, project_type_data, project_type_id):
        project_type = ProjectTypeModel.query.get_or_404(project_type_id)
        if project_type:
            if project_type_data.get("name", None):
                project_type.name = project_type_data["name"]
            if project_type_data.get("description", None):
                project_type.description = project_type_data["description"]
        else:
            project_type = ProjectTypeModel(id=project_type_id, **project_type_data)
        db.session.add(project_type)
        db.session.commit()
        return project_type

    @blp.response(
        202,
        description="Помечает поле is_deleted как True - мягкое удаления. Запись не удаляется из бд",
        example={"message": "тип проекта удален(мягко)."}
    )
    @blp.alt_response(404, description="Тип проекта не найден.")
    @blp.alt_response(400,
                      description="Данный статус возвращается если тип проекта еще назначен на какой нибудь проект."
                                  "В данном случае тип проекта нельзя удалять.")
    def delete(self, project_type_id):
        project_type = ProjectTypeModel.query.get_or_404(project_type_id)
        name = project_type.name

        if not project_type.projects:
            project_type.is_deleted = True
            db.session.add(project_type)
            db.session.commit()
            return {"message": f"Тип проекта '{name}' удален(мягко)."}
        abort(
            400,
            message="Удалить тип проекта не смогли. "
                    "Удостоверьтесь что у данного типа нет привязанных проектов."
        )

    @blp.response(200, ProjectTypeSchema)
    def post(self, project_type_id):
        project_type = ProjectTypeModel.query.get_or_404(project_type_id)
        if project_type.is_deleted:
            project_type.is_deleted = False
        else:
            abort(400, message="Указанный вами тип проекта и так не был удален. Восстанавливать нечего.")
        db.session.add(project_type)
        db.session.commit()
        return project_type


@blp.route("/project_type/hard_delete/<int:project_type_id>")
class HardDeleteProjectType(MethodView):
    @blp.response(
        202,
        description="Полностью удаляет запись из базы.",
        example={"message": "тип проекта удален безвозвратно."}
    )
    @blp.alt_response(404, description="Тип проекта не найден.")
    @blp.alt_response(400,
                      description="Данный статус возвращается если тип проекта еще назначен на какой нибудь проект."
                                  "В данном случае тип проекта нельзя удалять.")
    def delete(self, project_type_id):
        project_type = ProjectTypeModel.query.get_or_404(project_type_id)
        name = project_type.name

        if not project_type.projects:
            db.session.delete(project_type)
            db.session.commit()
            return {"message": f"Тип проекта '{name}' удален безвозвратно."}
        abort(
            400,
            message="Удалить тип проекта не смогли. "
                    "Удостоверьтесь что у данного типа нет привязанных проектов."
        )
