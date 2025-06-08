from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("MONGO_DB_NAME")]
products_collection = db["products"]


class Product:
    def __init__(
        self,
        id,
        seoName,
        name,
        price,
        uomName,
        description,
        image,
        mediaItems,
        category,
        salePrice,
    ):
        self.id = id
        self.seoName = seoName
        self.name = name
        self.description = description
        self.uomName = uomName
        self.price = price
        self.salePrice = salePrice
        self.mediaItems = mediaItems
        self.image = image
        self.category = category

    def to_dict(self):
        return {
            "id": self.id,
            "seoName": self.seoName,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "uomName": self.uomName,
            "image": self.image,
            "category": self.category,
            "salePrice": self.salePrice,
            "mediaItems": self.mediaItems,
        }

    def save(self):
        if not products_collection.find_one({"id": self.id}):
            products_collection.insert_one(self.to_dict())

    @classmethod
    def get_by_category(cls, category):
        cursor = products_collection.find({"category": category})
        return [cls(**doc) for doc in cursor]

    @classmethod
    def get_all(cls):
        cursor = products_collection.find()
        return [cls(**doc) for doc in cursor]
