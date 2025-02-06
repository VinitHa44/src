from bson import ObjectId
from app.models.domain.order import Order
from app.config.database import db

class OrderRepository:
    @staticmethod
    async def create_order(order: Order):
        order_dict = order.__dict__
        result = await db.db["orders"].insert_one(order_dict)
        return str(result.inserted_id)

    @staticmethod
    async def get_orders_by_user(user_id: str):
        user_id_obj = ObjectId(user_id)
        orders = await db.db["orders"].find({"user_id": user_id_obj}).to_list(None)
        return orders

    @staticmethod
    async def get_order_by_id(order_id: str):
        return await db.db["orders"].find_one({"_id": ObjectId(order_id)})
