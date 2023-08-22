from datetime import datetime

from core.db import db


class ProjectModel(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.String(2000), nullable=True)
    budget = db.Column(db.Integer, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    is_deleted = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    users = db.relationship("UserModel", back_populates="projects", secondary="projects_positions_users", viewonly=True)
    project_type_id = db.Column(db.Integer, db.ForeignKey("project_types.id"), unique=False)
    project_type = db.relationship("ProjectTypeModel", back_populates="projects")
    channels = db.relationship("ChannelModel", back_populates="project")

    def __repr__(self):
        return f"<Project: {self.name}>"
