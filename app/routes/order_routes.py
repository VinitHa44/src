from fastapi import APIRouter
from app.controllers.order_controller import router as order_router

order_api_router = APIRouter()
order_api_router.include_router(order_router, prefix="/orders", tags=["Orders"])
