from pymongo import MongoClient
from typing import List, Dict, Optional
import os


class ProductService:
    def __init__(
        self,
    ):
        self.client = MongoClient(os.getenv("MONGO_URI"))
        self.db = self.client[os.getenv("MONGO_DB_NAME")]
        self.products_collection = self.db["products"]

    def _serialize_product(self, product: Dict) -> Dict:
        """
        Convert MongoDB product document's ObjectId to string for JSON serialization.

        Args:
            product (Dict): A product document from MongoDB.

        Returns:
            Dict: The product document with the '_id' field converted to a string.
        """
        product = product.copy()
        if "_id" in product:
            product["_id"] = str(product["_id"])
        return product

    def get_products_by_category(
        self,
        category: str,
        page: int = 1,
        page_size: int = 10,
        sort_field: str = "name",
        ascending: bool = True,
    ) -> List[Dict]:
        """
        Get products by category with pagination.

        Args:
            category (str): Category name to filter.
            page (int): Page number, starts at 1.
            page_size (int): Number of items per page.
            sort_field (str): Field name to sort by.
            ascending (bool): Sort order.

        Returns:
            List[Dict]: List of product documents.
        """
        skip = (page - 1) * page_size
        sort_order = 1 if ascending else -1

        cursor = (
            self.products_collection.find({"category": category})
            .sort(sort_field, sort_order)
            .skip(skip)
            .limit(page_size)
        )
        products = [self._serialize_product(prod) for prod in cursor]
        return products
