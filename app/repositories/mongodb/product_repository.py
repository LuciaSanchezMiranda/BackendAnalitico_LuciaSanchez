"""Repository for product master data stored in MongoDB."""

import os
import re

from app.database.mongodb import get_mongodb_database


class ProductRepository:
    def get_product_by_id(self, product_id):
        """Find a product across the documented and existing collection shapes."""
        product_ids = [str(product_id)]

        # The current seed data uses SQL IDs like P004 and Mongo IDs like PL-0004.
        match = re.fullmatch(r"P(\d+)", str(product_id))
        if match:
            product_ids.append(f"PL-{int(match.group(1)):04d}")

        database = get_mongodb_database()
        preferred = os.getenv("MONGO_PRODUCTS_COLLECTION", "products")
        collection_names = [preferred]
        fallback = "product" if preferred != "product" else "products"
        collection_names.append(fallback)

        query = {
            "$or": [
                {"product_id": {"$in": product_ids}},
                {"_id": {"$in": product_ids}},
            ]
        }
        for collection_name in collection_names:
            product = database[collection_name].find_one(query)
            if product:
                return product
        return None
