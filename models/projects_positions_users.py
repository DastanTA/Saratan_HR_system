from datetime import datetime

from db import db


class PositionsUsers(db.Model):
    __tablename__ = "projects_positions_users"

    id = db.Column(db.Integer, primary_key=True)

    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))
    position_id = db.Column(db.Integer, db.ForeignKey("positions.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=True)
