from .db import db


class RecCenterRoom(db.Model):
    __tablename__ = "rec_center_room"

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
