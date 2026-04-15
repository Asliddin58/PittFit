from argon2.exceptions import VerifyMismatchError
from flask import Blueprint, jsonify, request
from functools import wraps
from models.db import db, ph
from models.user import User
import datetime
import jwt
import os

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")
auth_bp = Blueprint("auth_bp", import_name=__name__)

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
    if not email.endswith("@pitt.edu"):
        return jsonify({"error": "Must use a Pitt email address"}), 401

    password = request_json["password"]

    username = email.replace("@pitt.edu", "")
    registered_user = db.session.execute(
        db.select(User).filter_by(pitt_email=email)
    ).scalar_one_or_none()

    if not registered_user:
        hashed = ph.hash(password)
        user = User(pitt_email=email, password_hash=hashed)
        db.session.add(user)
        db.session.commit()
        status_code = 201  # new user entry created in table
    else:
        try:
            ph.verify(registered_user.password_hash, password)
        except VerifyMismatchError:
            return jsonify({"error": "Invalid credentials"}), 401
        status_code = 200

    payload = {
        "sub": username,
        "email": email,
        "iat": datetime.datetime.now(datetime.timezone.utc),
        "exp": datetime.datetime.now(datetime.timezone.utc)
        + datetime.timedelta(hours=1),
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    active_tokens.add(token)
    return jsonify({"token": token}), status_code


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
