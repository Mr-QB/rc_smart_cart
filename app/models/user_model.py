from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("MONGO_DB_NAME")]
users_collection = db["users"]


class User:
    def __init__(self, phone_number: str):
        self.phone_number = phone_number

    def save(self):
        if not users_collection.find_one({"phone_number": self.phone_number}):
            users_collection.insert_one({"phone_number": self.phone_number})

    @classmethod
    def get_by_phone(cls, phone_number: str):
        data = users_collection.find_one({"phone_number": phone_number})
        if data:
            return cls(phone_number=data["phone_number"])
        return None
