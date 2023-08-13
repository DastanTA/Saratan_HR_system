from datetime import datetime

from db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=True)
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(300))
    phone = db.Column(db.Integer, unique=True, nullable=True)
    first_name = db.Column(db.String(30))
    middle_name = db.Column(db.String(30))
    last_name = db.Column(db.String(50))
    basic_profession = db.Column(db.String(30)) #специализация. В чем лучше разбирается
    notes = db.column(db.String(5000), nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), unique=False)
    role = db.relationship("RoleModel", back_populates="users")
    occupancy_id = db.Column(db.Integer, db.ForeignKey("occupancies.id"), unique=False)
    occupancy = db.relationship("OccupancyModel", back_populates="users")
    positions = db.relationship("PositionModel", back_populates="users", secondary="projects_positions_users")
    projects = db.relationship("ProjectModel", back_populates="users", secondary="projects_positions_users")
    channels = db.relationship("ChannelModel", back_populates="manager", nullable=True)

    def __repr__(self):
        return f"<{self.first_name} {self.last_name}>"
