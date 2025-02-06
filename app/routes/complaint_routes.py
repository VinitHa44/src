from fastapi import APIRouter
from app.controllers.complaint_controller import router as compliant_router

compliant_api_router = APIRouter()
compliant_api_router.include_router(compliant_router, prefix="/complaints", tags=["Complaints"])



