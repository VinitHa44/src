from datetime import datetime
from app.config.database import db
from app.models.domain.cart import Cart
from bson import ObjectId

class CartRepository:

    @staticmethod
    async def get_cart_by_user_id(user_id: str):
        print(f"\n\n\nuser_id: {user_id}")
        return await db.db["carts"].find({"user_id": ObjectId(user_id)}).to_list(None)
    
    @staticmethod
    async def get_cart(user_id: str):
        cart = await db.db["carts"].find_one({"user_id": ObjectId(user_id)})
        if cart:
            cart["cart_id"] = str(cart.pop("_id"))  # Convert `_id` to `cart_id`
            cart["user_id"] = str(cart["user_id"])
            for item in cart["items"]:
                item["product_id"] = str(item["product_id"])
            return cart
        return None

    @staticmethod
    async def add_to_cart(user_id: str, items: list):
        cart = await db.db["carts"].find_one({"user_id": ObjectId(user_id)})

        if cart:
            for item in items:
                found = False
                for cart_item in cart["items"]:
                    if cart_item["product_id"] == ObjectId(item.product_id):
                        cart_item["quantity"] += item.quantity
                        found = True
                        break
                
                if not found:
                    cart["items"].append({"product_id": ObjectId(item.product_id), "quantity": item.quantity})

            cart["updated_at"] = datetime.utcnow()
            await db.db["carts"].update_one({"_id": cart["_id"]}, {"$set": cart})
        else:
            new_cart = {
                "user_id": ObjectId(user_id),
                "items": [{"product_id": ObjectId(item.product_id), "quantity": item.quantity} for item in items],
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            }
            await db.db["carts"].insert_one(new_cart)

        return {"message": "Products added to cart successfully"}

    @staticmethod
    async def remove_from_cart(user_id: str, product_id: str):
        cart = await db.db["carts"].find_one({"user_id": ObjectId(user_id)})
        if not cart:
            return {"error": "Cart not found"}

        cart["items"] = [item for item in cart["items"] if item["product_id"] != ObjectId(product_id)]
        cart["updated_at"] = datetime.utcnow()

        await db.db["carts"].update_one({"_id": cart["_id"]}, {"$set": {"items": cart["items"], "updated_at": cart["updated_at"]}})

        return {"message": "Product removed from cart successfully"}
