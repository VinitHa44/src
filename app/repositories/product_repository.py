from bson import ObjectId
from app.config.database import db
from app.models.domain.product import Product
import random

class ProductRepository:

    @staticmethod
    async def insert_product(product_data: dict):
        result = await db.db["products"].insert_one(product_data)
        return str(result.inserted_id)
    
    # @staticmethod
    # async def preload_products(products: list):
    #     await db.db["products"].insert_many(products)

    @staticmethod
    async def create_product(product: Product):
        product_dict = product.__dict__
        result = await db.db["products"].insert_one(product_dict)
        
        created_product = await db.db["products"].find_one({"_id": result.inserted_id})
        
        if created_product:
            created_product["product_id"] = str(created_product.pop("_id"))  # Rename _id -> product_id
            created_product["seller_id"] = str(created_product["seller_id"])  # Convert ObjectId to string

            return created_product
        
        return None

    @staticmethod
    async def get_all_products():
        products_cursor = db.db["products"].find()
        products = await products_cursor.to_list(length=None)
        for product in products:
            product["product_id"] = str(product.pop("_id"))
            product["seller_id"] = str(product["seller_id"])
        return products

    @staticmethod
    async def get_product_by_id(product_id: str):
        product = await db.db["products"].find_one({"_id": ObjectId(product_id)})
        if product:
            product["product_id"] = str(product.pop("_id"))
            product["seller_id"] = str(product["seller_id"])
        return product
    
    @staticmethod
    async def get_products_by_ids(product_ids: list):
        # Convert product_ids to ObjectId if they are in string format
        object_ids = [ObjectId(pid) if isinstance(pid, str) else pid for pid in product_ids]

        # Query to get all products with the matching product_ids
        products = await db.db["products"].find({"_id": {"$in": object_ids}}).to_list(length=None)

        return products

    @staticmethod
    async def delete_product(product_id: str):
        result = await db.db["products"].delete_one({"_id": ObjectId(product_id)})
        return result.deleted_count > 0
    
    @staticmethod
    async def update_product(product_id: str, product_data: dict, seller_id: str):
        product_data["seller_id"] = str(ObjectId(seller_id))
        result = await db.db["products"].update_one({"_id": ObjectId(product_id)}, {"$set": product_data})
        if result.modified_count == 0:
            return None
        updated_product = await db.db["products"].find_one({"_id": ObjectId(product_id)})

        if updated_product:
            # Convert `_id` to `product_id`
            updated_product["product_id"] = str(updated_product["_id"])
            del updated_product["_id"]  # Remove `_id` to avoid conflicts

        return updated_product
    
    @staticmethod
    async def get_seller_id(product_id: str):
        product = await db.db["products"].find_one({"_id": ObjectId(product_id)})
        return product.get("seller_id") if product else None
    