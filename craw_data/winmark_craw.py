import requests
from app.models.product_model import Product
import json

# List of slugs (categories) to scrape
slugs = [
    "van-phong-pham-do-choi--c27",
    "sua-cac-loai--c08",
    "rau-cu-trai-cay--c02",
    "hoa-pham-tay-rua--c10",
    "cham-soc-ca-nhan--c11",
    "thit-hai-san-tuoi--c03",
    "banh-keo--c07",
    "do-uong-co-con--c31",
    "do-uong-giai-khat--c09",
]

url = "https://api-crownx.winmart.vn/it/api/web/v3/item/category"
all_items = []
try:
    max_product = Product.objects().order_by("-product_id").first()
    current_id = max_product.product_id + 1 if max_product else 1
except Exception:
    current_id = 1
for slug in slugs:
    print(f"🔍 Scraping category: {slug}")
    # Scrape 200 products (20 pages with 10 products per page)
    for page in range(1, 21):
        params = {
            "pageNumber": page,
            "pageSize": 10,
            "slug": slug,
            "storeCode": 1535,
            "storeGroupCode": 1998,
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            prod_info_data = response.json().get("data", {}).get("items", [])
            print(f"[Page {page}] Retrieved {len(prod_info_data)} products.")

            for item in prod_info_data:
                if not item.get("seoName"):
                    continue

                detai_prod_url = (
                    f"https://winmart.vn/_next/data/CPh75ZmY3r_j4funwLmH7/products/"
                    f"{item.get('seoName')}.json?storeCode=1535&storeGroupCode=1998&slug={item.get('seoName')}"
                )

                try:
                    detail_resp = requests.get(detai_prod_url)
                    detail_data = detail_resp.json()
                    description = (
                        detail_data.get("pageProps", {})
                        .get("product", {})
                        .get("longDescription", "")
                    )
                except Exception:
                    description = ""

                # Create and save the product object
                product = Product(
                    id=current_id,
                    seoName=item.get("seoName"),
                    name=item.get("name"),
                    uomName=item.get("uomName"),
                    description=description,
                    price=item.get("price"),
                    salePrice=item.get("salePrice"),
                    image=item.get("mediaUrl"),
                    category=item.get("categoryName"),
                    mediaItems=item.get("mediaItems"),
                )
                product.save()
                current_id += 1

                # Store item for writing to JSON later
                all_items.append(item)

        except requests.exceptions.RequestException as e:
            print(f"Error calling API on page {page} for slug '{slug}': {e}")

# Write all collected products to JSON file
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(all_items, f, ensure_ascii=False, indent=4)

print(f"Saved {len(all_items)} products to data.json.")
