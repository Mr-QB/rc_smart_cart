from flask import Blueprint, request, jsonify
from ..services.auth_service import sendOtp

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/otp_send", methods=["POST"])
def otpSent():
    data = request.get_json()
    if not data or "phone_number" not in data:
        return jsonify({"error": "Phone number is required"}), 400
    phone_number = data["phone_number"]

    return jsonify({"message": "Login endpoint"})


@auth_bp.route("/register", methods=["POST"])
def register():
    return jsonify({"message": "Register endpoint"})
