from ..models.user import User
from app import db
from flask import jsonify
from flask_jwt_extended import create_access_token
from datetime import timedelta
from werkzeug.security import check_password_hash

def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        return jsonify({"error": "User not found"}), 404

def login_user(email, password):
    user = User.query.filter_by(email=email).first()

    # ✅ Use check_password_hash to compare hashed password
    if user and check_password_hash(user.password_hash, password):
        access_token = create_access_token(
            identity={"id": user.id, "email": user.email},
            additional_claims={"role": user.role},
            expires_delta=timedelta(hours=1)
        )
        return jsonify({
            "access_token": access_token,
            "user": user.to_dict()
        }), 200

    return jsonify({"error": "Invalid credentials"}), 401
