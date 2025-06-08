from flask import Blueprint, request, jsonify
from ..services.product_service import ProductService

prod_bp = Blueprint("product-data", __name__)


@prod_bp.route("/category", methods=["GET"])
def get_products():
    category = request.args.get("category")
    page_size = request.args.get("page_size", default=10, type=int)
    print(page_size)
    if not category:
        return jsonify({"error": "Missing 'category' parameter"}), 400

    try:
        products = ProductService().get_products_by_category(
            category=category,
            page=1,
            page_size=int(page_size),
        )
        return jsonify(products), 200
    except Exception as e:
        print(f"Error fetching products: {e}")
        return jsonify({"error": str(e)}), 500
