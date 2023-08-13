from datetime import datetime

from db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    phone = db.Column(db.Integer, unique=True, nullable=True)
    first_name = db.Column(db.String(30), nullable=False)
    middle_name = db.Column(db.String(30), nullable=True)
    last_name = db.Column(db.String(50), nullable=False)
    basic_profession = db.Column(db.String(30), nullable=False) #специализация. В чем лучше разбирается
    notes = db.column(db.String(5000), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), unique=False, nullable=False)
    role = db.relationship("RoleModel", back_populates="users")
    occupancy_id = db.Column(db.Integer, db.ForeignKey("occupancies.id"), unique=False, nullable=False)
    occupancy = db.relationship("OccupancyModel", back_populates="users")
    positions = db.relationship("PositionModel", back_populates="users", secondary="positions_users")

    def __repr__(self):
        return f"<{self.first_name} {self.last_name}>"
