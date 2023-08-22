from datetime import datetime

from core.db import db


class ProjectTypeModel(db.Model):
    __tablename__ = "project_types"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.String(2000), nullable=True)
    is_deleted = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    projects = db.relationship(
        "ProjectModel",
        back_populates="project_type",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Project_type: {self.name}>"
