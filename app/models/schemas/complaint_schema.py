from typing import Optional, Literal
from pydantic import BaseModel

class ComplaintCreate(BaseModel):
    user_id: str
    order_id: str
    product_id: str
    issue: str
    image_url: Optional[str] = None

class ComplaintResponse(BaseModel):
    complaint_id: str
    user_id: str
    order_id: str
    product_id: str
    issue: str
    image_url: Optional[str]
    status: Literal["open", "rejected"]
