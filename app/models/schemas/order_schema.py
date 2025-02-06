from typing import List, Literal
from pydantic import BaseModel
from bson import ObjectId

class OrderItemSchema(BaseModel):
    product_id: str  # Store as string since ObjectId is BSON-specific
    quantity: int
    price: float

class OrderSchema(BaseModel):
    user_id: str
    items: List[OrderItemSchema]
    total_amount: float
    status: Literal["pending", "shipped", "delivered", "cancelled"]
