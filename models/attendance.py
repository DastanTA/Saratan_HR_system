from db import db


class AttendanceModel(db.Model):
    __tablename__ = "attendance"

    id = db.Column(db.Integer, primary_key=True)
    entrance_date_time = db.Column(db.DateTime)
    exit_date_time = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=False)
