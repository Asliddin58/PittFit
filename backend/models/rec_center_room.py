from .db import db

class RecCenterRoom(db.Model):
    __tablename__ = "rec_center_room"

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False, default=0)
    current_occupancy = db.Column(db.Integer, nullable=False, default=0)
    opening_time = db.Column(db.Time, nullable=True)
    closing_time = db.Column(db.Time, nullable=True)