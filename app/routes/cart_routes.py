from fastapi import APIRouter
from app.controllers.cart_controller import router as cart_router

cart_api_router = APIRouter()
cart_api_router.include_router(cart_router, prefix="/cart", tags=['Cart'])