import os
from zlapi import ZaloAPI
from zlapi.models import *
import json


def sendOtp(phone_number: str, otp: str, otp_type=None) -> bool:
    """
    Sends an OTP to a given phone number.
    Args:
        phone_number (str): The recipient's phone number.
        otp (str): The OTP to be sent.
    Returns:
        bool: True if the OTP was sent successfully, False otherwise.
    """

    def sendOtpSms(
        phone_number: str,
        otp: str,
    ) -> bool:
        """
        Sends an OTP to a given phone number via SMS.

        Args:
            phone_number (str): The recipient's phone number.
            otp (str): The OTP to be sent.

        Returns:
            bool: True if the OTP was sent successfully, False otherwise.
        """
        pass
        return False

    def sendOtpZalo(
        phone_number: str,
        otp: str,
    ) -> bool:
        """
        Sends an OTP to a given phone number using the Zalo API.

        Args:
            phone_number (str): The recipient's phone number.
            otp (str): The OTP to be sent.

        Returns:
            None
        """
        try:
            imei = os.getenv("ZALO_IMEI")
            cookies = json.loads(os.getenv("ZALO_COOKIES"))
            zalo_phone_number = os.getenv("ZALO_PHONE_NUMBER")
            zalo_password = os.getenv("ZALO_PASSWORD")

            bot = ZaloAPI(zalo_phone_number, zalo_password, imei=imei, cookies=cookies)
            bot.sendMessage(
                message=Message(
                    "Mã xác thực của bạn là: "
                    + otp
                    + ". Vui lòng không chia sẻ mã này với bất kỳ ai."
                ),
                thread_id=bot.fetchPhoneNumber(str(phone_number)).uid,
                thread_type=ThreadType.USER,
            )
            return True
        except Exception as e:
            print(f"Error sending OTP via Zalo: {e}")
            return False

    if otp_type == "zalo_otp":
        return sendOtpZalo(phone_number, otp)
    else:
        return sendOtpSms(phone_number, otp)
