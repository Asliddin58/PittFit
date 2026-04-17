from .db import db


class WorkoutLog(db.Model):
    __tablename__ = "workout_log"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.String(), nullable=True)
