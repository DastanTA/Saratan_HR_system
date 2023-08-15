from datetime import datetime

from db import db


class PositionModel(db.Model):
    __tablename__ = "positions"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String(2000), nullable=True)
    is_deleted = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    users = db.relationship("UserModel", back_populates="positions", secondary="projects_positions_users")

    def __repr__(self):
        return f"<Position: {self.name}>"
