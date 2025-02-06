from fastapi import APIRouter, Depends, HTTPException
from app.repositories.cart_repository import CartRepository
from app.repositories.product_repository import ProductRepository
from app.usecases.order_usecase import OrderUseCase
from app.utils.auth_utils import get_current_user
from app.models.schemas.order_schema import OrderSchema

router = APIRouter()

@router.post("/", response_model=dict)
async def place_order(user: dict = Depends(get_current_user)):
    if user["role"] != "buyer":
        raise HTTPException(status_code=403, detail="Only buyers can place orders")

    # Fetch user's cart items from the database
    cart_items = await CartRepository.get_cart_by_user_id(user["id"])
    
    if not cart_items:
        raise HTTPException(status_code=400, detail="Your cart is empty")

    # Prepare to fetch product details (like price) for each item
    product_ids = [str(item["product_id"]) for cart in cart_items for item in cart["items"]]
    
    # Fetch product prices (assuming you have a method to get multiple products)
    products = await ProductRepository.get_products_by_ids(product_ids)

    # Map product ID to its price for quick lookup
    product_prices = {str(product["_id"]): product["price"] for product in products}

    # Update cart items with price information
    updated_cart_items = []
    for cart in cart_items:
        for item in cart["items"]:
            price = product_prices.get(str(item["product_id"]), 0)  # Default to 0 if price is not found
            updated_cart_items.append({
                "product_id": str(item["product_id"]),
                "quantity": item["quantity"],
                "price": price
            })
    print(f"Updated Cart Items: {updated_cart_items}") 
    # Pass updated cart items to OrderUseCase
    response = await OrderUseCase.place_order(user["id"], updated_cart_items)
    
    if "error" in response:
        raise HTTPException(status_code=400, detail=response["error"])

    return response

@router.get("/", response_model=list)
async def get_orders(user: dict = Depends(get_current_user)):
    if user["role"] != "buyer":
        raise HTTPException(status_code=403, detail="Only buyers can view orders")
    
    return await OrderUseCase.get_orders(user["id"])

@router.get("/{order_id}", response_model=OrderSchema)
async def get_order_details(order_id: str, user: dict = Depends(get_current_user)):
    if user["role"] != "buyer":
        raise HTTPException(status_code=403, detail="Only buyers can view order details")

    response = await OrderUseCase.get_order_details(order_id)
    if "error" in response:
        raise HTTPException(status_code=404, detail=response["error"])
    return response