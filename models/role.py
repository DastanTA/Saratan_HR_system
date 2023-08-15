from datetime import datetime

from db import db


class RoleModel(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.String(2000), nullable=True)
    is_deleted = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    users = db.relationship("UserModel", back_populates="role", lazy="dynamic", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Role: {self.name}>"
