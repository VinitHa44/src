from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas.cart_schema import CartRequestSchema
from app.usecases.cart_usecase import CartUseCase
from app.utils.auth_utils import get_current_user

router = APIRouter()

@router.post("/add", response_model=dict)
async def add_to_cart(cart_data: CartRequestSchema, user: dict = Depends(get_current_user)):
    if user["role"] != "buyer":
        raise HTTPException(status_code=403, detail="Only buyers can add products to cart")

    response = await CartUseCase.add_to_cart(user["id"], cart_data.items)
    if "error" in response:
        raise HTTPException(status_code=400, detail=response["error"])
    return response

@router.delete("/remove/{product_id}", response_model=dict)
async def remove_from_cart(product_id: str, user: dict = Depends(get_current_user)):
    if user["role"] != "buyer":
        raise HTTPException(status_code=403, detail="Only buyers can remove products from cart")
    return await CartUseCase.remove_from_cart(user["id"], product_id)

@router.get("/", response_model=dict)
async def get_cart(user: dict = Depends(get_current_user)):
    if user["role"] != "buyer":
        raise HTTPException(status_code=403, detail="Only buyers can view their cart")
    return await CartUseCase.get_cart(user["id"])
