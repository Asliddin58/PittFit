from flask import Blueprint, jsonify
from models import RecCenterRoom

occupancy_bp = Blueprint("occupancy", __name__)

@occupancy_bp.route("/", methods=["GET"])
def get_occupancy():
    rooms = RecCenterRoom.query.all()

    result = []

    for room in rooms:
        capacity = room.capacity or 0
        current = room.current_occupancy or 0

        percent = 0
        if capacity > 0:
            percent = round((current / capacity) * 100, 2)

        result.append({
            "id": room.id,
            "location": room.location,
            "type": room.type,
            "current_occupancy": current,
            "capacity": capacity,
            "occupancy_percent": percent,
            "hours": {
                "open": str(room.opening_time) if room.opening_time else None,
                "close": str(room.closing_time) if room.closing_time else None
            }
        })

    return jsonify({"facilities": result}), 200