from flask import Blueprint, request, jsonify
from ..controllers.user_controller import get_user_by_id, login_user
from flask_jwt_extended import jwt_required, get_jwt_identity
import pandas as pd

user_bp = Blueprint("user_bp", __name__)

@user_bp.route("/<int:user_id>", methods=["GET"])
@jwt_required()  # ✅ Protect this route
def get_user(user_id):
    return get_user_by_id(user_id)

@user_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    return login_user(email, password)


@user_bp.route("/upload", methods=["POST"])
def upload_files():
    uploaded_files = request.files.getlist("files")
    
    if not uploaded_files:
        return jsonify({"error": "No files uploaded"}), 400

    column_sets = []
    file_names = []

    for file in uploaded_files:
        file_names.append(file.filename)
        try:
            if file.filename.endswith(".csv"):
                df = pd.read_csv(file)
            elif file.filename.endswith((".xls", ".xlsx")):
                df = pd.read_excel(file)
            else:
                return jsonify({"error": f"Unsupported file type: {file.filename}"}), 400

            column_sets.append(set(df.columns))
        except Exception as e:
            return jsonify({"error": f"Failed to read {file.filename}: {str(e)}"}), 500

    # Check if all files have the same columns
    all_same = all(cols == column_sets[0] for cols in column_sets)

    return jsonify({
        "all_same_columns": all_same,
        "columns_per_file": {file_names[i]: list(column_sets[i]) for i in range(len(file_names))}
    })


# Example protected route (test JWT)
@user_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    current_user = get_jwt_identity()  # this is what you passed to `identity=`
    return {"message": "You are logged in!", "user": current_user}, 200
