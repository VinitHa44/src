from pydantic import BaseModel
from typing import List

class CartItemSchema(BaseModel):
    product_id: str
    quantity: int

class CartRequestSchema(BaseModel):
    items: List[CartItemSchema]
