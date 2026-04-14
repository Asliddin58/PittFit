from flask import Blueprint, jsonify, request
from functools import wraps
import datetime
import jwt
import os

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")
auth_bp = Blueprint("auth_bp", import_name=__name__)

# FIXME: Store credentials in a database table that models users
credentials_dict = {
    "abc93": {"email": "abc93@pitt.edu", "password": "pass1"},
    "xyz12": {"email": "xyz12@pitt.edu", "password": "pass2"},
}

# FIXME: Store generated tokens in a database table
active_tokens = set()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"error": "No token"}), 401

        if token.startswith("Bearer "):
            token = token.split(" ", 1)[1]

        if token not in active_tokens:
            return jsonify({"error": "Not logged in"}), 401

        try:
            jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            active_tokens.discard(token)
            return jsonify({"error": "Expired token"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated


@auth_bp.route("/login", methods=["POST"])
def login():
    token = request.headers.get("Authorization")
    if token and token.startswith("Bearer "):
        token = token.split(" ", 1)[1]

    if token and token in active_tokens:
        return jsonify({"error": "Already logged in"}), 400

    request_json = request.get_json()
    email = request_json["email"]
    password = request_json["password"]

    username = email.replace("@pitt.edu", "")
    if (
        username not in credentials_dict
        or credentials_dict[username]["password"] != password
    ):
        return jsonify({"error": "Invalid credentials"}), 401

    payload = {
        "sub": username,
        "email": email,
        "iat": datetime.datetime.now(datetime.timezone.utc),
        "exp": datetime.datetime.now(datetime.timezone.utc)
        + datetime.timedelta(hours=1),
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    active_tokens.add(token)
    return jsonify({"token": token}), 200


@auth_bp.route("/logout", methods=["POST"])
@token_required
def logout():
    token = request.headers.get("Authorization")
    if token.startswith("Bearer "):
        token = token.split(" ", 1)[1]

    active_tokens.discard(token)
    return jsonify({"message": "Logged out"}), 200


@auth_bp.route("/me")
@token_required
def me():
    token = request.headers.get("Authorization")
    if token.startswith("Bearer "):
        token = token.split(" ", 1)[1]

    payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    return jsonify({"username": payload["sub"], "email": payload["email"]}), 200