from datetime import datetime

from db import db


class ChannelModel(db.Model):
    __tablename__ = "channels"

    id = db.Column(db.Integer, primary_key=True)
    is_original = db.Column(db.Boolean, default=True)
    channel_name = db.Column(db.String(150))
    description = db.Column(db.String(2000), nullable=True)
    url_address = db.Column(db.String(1000), unique=True)
    is_active = db.Column(db.Boolean, default=True)
    is_deleted = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    manager_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=False)
    manager = db.relationship("UserModel", back_populates="channels")
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), unique=False)
    project = db.relationship("ProjectModel", back_populates="channels")

    def __repr__(self):
        return f"<Channel: {self.name}>"
