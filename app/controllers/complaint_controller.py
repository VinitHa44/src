from fastapi import APIRouter, HTTPException
from app.usecases.complaint_usecase import ComplaintUseCase
from app.models.schemas.complaint_schema import ComplaintCreate, ComplaintResponse

router = APIRouter()

@router.post("/", response_model=dict)
async def file_complaint(complaint: ComplaintCreate):
    response = await ComplaintUseCase.file_complaint(complaint)
    return response
