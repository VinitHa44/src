from typing import List
from datetime import datetime

class Product:  
    def __init__(self, title: str, description: str, category: str, price: float, rating: float, brand: str, images: List[str], thumbnail: str, seller_id: str, created_at: datetime = None, updated_at: datetime = None):
        self.title = title
        self.description = description
        self.category = category
        self.price = price
        self.rating = rating
        self.brand = brand
        self.images = images
        self.thumbnail = thumbnail
        self.seller_id = seller_id
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
