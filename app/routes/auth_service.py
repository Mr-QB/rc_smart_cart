from flask import Blueprint, request, jsonify
from ..services.auth_service import sendOtp
from ..models.otp_model import OTP
from ..models.user_model import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/send-otp", methods=["POST"])
def otpSent():
    data = request.get_json()

    if not data or "phone_number" not in data:
        return jsonify({"error": "Phone number is required"}), 400

    phone_number = data["phone_number"]
    otp = OTP(phone_number=phone_number)
    otp.save()

    if sendOtp(phone_number, otp.otp, "zalo_otp"):

        return jsonify({"success": True, "message": "OTP sent successfully"}), 200
    else:
        return jsonify({"error": "Failed to send OTP"}), 500


@auth_bp.route("/verify-otp", methods=["POST"])
def verify_otp():
    data = request.get_json()

    if not data or "phone_number" not in data or "otp" not in data:
        return jsonify({"error": "Phone number and OTP are required"}), 400

    phone_number = data["phone_number"]
    otp_input = data["otp"]

    success, message = OTP.verify(phone_number, otp_input)

    if success:
        User(phone_number).save()
        return jsonify({"success": True, "message": message}), 200
    else:
        return jsonify({"success": False, "message": message}), 400
