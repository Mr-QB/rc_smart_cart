def sendOtp(phone_number: str, otp: str) -> bool:
    """
    Sends an OTP to a given phone number.
    Args:
        phone_number (str): The recipient's phone number.
        otp (str): The OTP to be sent.
    Returns:
        bool: True if the OTP was sent successfully, False otherwise.
    """

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
        # Placeholder for Zalo API integration
        pass
