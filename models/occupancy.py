from datetime import datetime

from db import db


class OccupancyModel(db.Model):
    __tablename__ = "occupancies"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True)
    description = db.Column(db.String(500), nullable=True)
    users = db.relationship("UserModel", back_populates="occupancy", lazy="dynamic", cascade="all, delete-orphan")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<{self.name}>"
