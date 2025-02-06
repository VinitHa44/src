from typing import List, Literal
from datetime import datetime
from bson import ObjectId

class OrderItem:
    def __init__(self, product_id: str, quantity: int, price: float):
        self.product_id = ObjectId(product_id)
        self.quantity = quantity
        self.price = price

class Order:
    def __init__(self, user_id: str, items: List[OrderItem], total_amount: float, status: Literal["pending", "shipped", "delivered", "cancelled"] = "pending"):
        self.user_id = ObjectId(user_id)
        self.items = [item.__dict__ for item in items]
        self.total_amount = total_amount
        self.status = status
        self.created_at = datetime.utcnow()
