from flask import Blueprint, jsonify
from models.db import db
from models.announcement import Announcement

announcement_bp = Blueprint("announcements_bp", __name__)


# Returns all active announcements in descending chronological order.
# Inactive announcements (is_active=False) are filtered out automatically.
# FR[2.4]: announcements displayed in descending chronological order.
@announcement_bp.route("/", methods=["GET"])
def get_announcements():
    announcements = (
        db.session.execute(
            db.select(Announcement)
            .where(Announcement.is_active == True)
            .order_by(Announcement.created_at.desc())
        )
        .scalars()
        .all()
    )

    return jsonify([a.to_dict() for a in announcements]), 200
