from .db import db

workout_template_equipment = db.Table(
    "workout_template_equipment",
    db.Column(
        "workout_template_id",
        db.Integer,
        db.ForeignKey("workout_template.id"),
        primary_key=True,
    ),
    db.Column(
        "equipment_id", db.Integer, db.ForeignKey("equipment.id"), primary_key=True
    ),
)


class WorkoutTemplate(db.Model):
    __tablename__ = "workout_template"

    id = db.Column(db.Integer, primary_key=True)
    workout_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
