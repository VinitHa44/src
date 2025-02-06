from typing import List, Optional
from pydantic import BaseModel, Field

class ProductCreateSchema(BaseModel):
    title: str  # Required
    description: Optional[str] = None
    category: Optional[str] = None
    price: float = Field(..., gt=0, description="Price must be greater than 0")
    rating: float = Field(..., ge=0, le=5, description="Rating must be between 0 and 5")
    brand: Optional[str] = None
    images: Optional[List[str]] = None
    thumbnail: Optional[str] = None

class ProductResponse(BaseModel): 
    product_id: str  
    title: str
    description: str
    category: str
    price: float
    rating: float
    brand: str
    images: List[str]
    thumbnail: str
    seller_id: str
