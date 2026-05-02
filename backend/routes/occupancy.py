from flask import Blueprint, jsonify
from sqlalchemy import select

from models import RecCenterRoom, db

occupancy_bp = Blueprint("occupancy", __name__)


# Returns current occupancy, capacity, and hours for each Rec Center facility.
# Calculates occupancy percentage dynamically. Returns empty list if no data seeded.
# FR[2.2]: real-time facility occupancy.
@occupancy_bp.route("/", methods=["GET"])
def get_occupancy():
    rooms = db.session.execute(select(RecCenterRoom)).scalars().all()

    result = []

    for room in rooms:
        capacity = room.capacity or 0
        current = room.current_occupancy or 0

        percent = 0
        if capacity > 0:
            percent = round((current / capacity) * 100, 2)

        result.append(
            {
                "id": room.id,
                "location": room.location,
                "type": room.type,
                "current_occupancy": current,
                "capacity": capacity,
                "occupancy_percent": percent,
                "hours": {
                    "open": str(room.opening_time) if room.opening_time else None,
                    "close": str(room.closing_time) if room.closing_time else None,
                },
            }
        )

    return jsonify({"facilities": result}), 200

