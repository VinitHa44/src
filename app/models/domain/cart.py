from datetime import datetime
from typing import List
from bson import ObjectId

class CartItem:
    def __init__(self, product_id: str, quantity: int):
        self.product_id = ObjectId(product_id)
        self.quantity = quantity

class Cart:
    def __init__(self, user_id: str, items: List[CartItem] = None, created_at: datetime = None, updated_at: datetime = None):
        self.user_id = ObjectId(user_id)
        self.items = items or []
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
