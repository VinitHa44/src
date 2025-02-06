from fastapi import APIRouter
from app.controllers.product_controller import router as product_router

product_api_router = APIRouter()
product_api_router.include_router(product_router, prefix="/products", tags=["Products"])
