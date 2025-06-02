from pymongo import MongoClient
from datetime import datetime, timedelta
import os
import random

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("MONGO_DB_NAME")]
otp_collection = db["otps"]


class OTP:
    def __init__(self, phone_number: str, otp: str = None, expire_at=None):
        self.phone_number = phone_number
        self.otp = otp
        self.expire_at = expire_at

    def save(self, ttl_seconds=300):
        if not self.otp:
            self.otp = f"{random.randint(100000, 999999)}"
        self.expire_at = datetime.utcnow() + timedelta(seconds=ttl_seconds)
        otp_collection.update_one(
            {"phone_number": self.phone_number},
            {"$set": {"otp": self.otp, "expire_at": self.expire_at}},
            upsert=True,
        )

    @classmethod
    def verify(self, phone_number: str, otp_input: str):
        record = otp_collection.find_one({"phone_number": phone_number})
        if not record:
            return False, "OTP not found"

        if datetime.utcnow() > record["expire_at"]:
            return False, "OTP expired"

        if record["otp"] != otp_input:
            return False, "Incorrect OTP"

        otp_collection.delete_one({"phone_number": phone_number})
        return True, "OTP verified"
