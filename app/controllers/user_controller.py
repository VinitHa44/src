from fastapi import APIRouter, Depends, HTTPException
from app.usecases.user_usecase import UserUseCase
from app.models.schemas.user_schema import UserCreate, UserLogin, Token

router = APIRouter()

@router.post("/register", response_model=dict)
async def register_user(user: UserCreate):
    response = await UserUseCase.register_user(user)
    if "error" in response:
        raise HTTPException(status_code=400, detail=response["error"])
    return response

@router.post("/login", response_model=Token)
async def login_user(user: UserLogin):
    response = await UserUseCase.login_user(user)
    if "error" in response:
        raise HTTPException(status_code=401, detail=response["error"])
    return response
