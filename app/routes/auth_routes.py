from fastapi import APIRouter
from app.controllers.user_controller import router as user_router

auth_router = APIRouter()
auth_router.include_router(user_router, prefix="/auth", tags=["Authentication"])
