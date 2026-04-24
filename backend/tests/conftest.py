import pytest
from flask import Flask, request, jsonify

@pytest.fixture
def client():
    app = Flask(__name__)

    @app.route("/auth/login", methods=["POST"])
    def login():
        data = request.get_json()

        if not data or "email" not in data or "password" not in data:
            return jsonify({"error": "missing fields"}), 400

        if data["password"] == "correctpassword":
            return jsonify({"message": "success"}), 200

        return jsonify({"error": "unauthorized"}), 401

    with app.test_client() as client:
        yield client