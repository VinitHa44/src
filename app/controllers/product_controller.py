import json
import os
from typing import Annotated, List, Optional
from bson import ObjectId
from fastapi import APIRouter, Depends, Form, HTTPException, Response, UploadFile, File
from fastapi.responses import FileResponse
from app.usecases.product_usecase import ProductUseCase
from app.models.schemas.product_schema import ProductResponse
from app.utils.auth_utils import get_current_user 
import shutil

from app.utils.gd_utils import upload_to_google_drive

router = APIRouter()

@router.post("/preload-products", response_model=dict)
async def preload_products():
    predefined_seller_ids = [
        str(ObjectId("67a36a669243387ce0f5cbef")), 
        str(ObjectId("67a36a739243387ce0f5cbf0")),
        str(ObjectId("67a36d635c6800c3fdc06c4d"))
    ]
    response = await ProductUseCase.preload_products(predefined_seller_ids)
    return response

@router.post("/", response_model=ProductResponse)
async def create_product(file: UploadFile = File(...),
    product_data: str = Form(...),  # Expecting JSON string
    user: dict = Depends(get_current_user),):
    if user["role"] != "seller":
        raise HTTPException(status_code=403, detail="Only sellers can add products")

    try:
        print(f"Received product_data: {product_data}")  # Debugging
        product_dict = json.loads(product_data)  # Convert string to dictionary
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format in product_data")

    return await ProductUseCase.create_product(product_dict, file, user["id"])

@router.get("/", response_model=List[ProductResponse])
async def get_all_products():
    return await ProductUseCase.get_all_products()

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str):
    return await ProductUseCase.get_product_by_id(product_id)

@router.delete("/{product_id}", response_model=dict)
async def delete_product(product_id: str, user: dict = Depends(get_current_user)):
    if user["role"] not in ["admin", "seller"]:
        raise HTTPException(status_code=403, detail="Only admins and sellers can delete products")
    
    return await ProductUseCase.delete_product(product_id, user)

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: str,
    product_data: str = Form(...),
    file: Optional[UploadFile] = File(None),
    user: dict = Depends(get_current_user),
):
    if user["role"] != "seller":
        raise HTTPException(status_code=403, detail="Only sellers can update products")

    try:
        product_dict = json.loads(product_data)  # Convert string to dictionary
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format in product_data")

    return await ProductUseCase.update_product(product_id, product_dict, file, user["id"])

@router.get("/download/{product_id}")
async def download_product_details(product_id: str):
    # Fetch product details
    product = await ProductUseCase.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Convert the product to a JSON-serializable format
    file_path = f"temp/product_{product_id}.json"
    with open(file_path, "w") as file:
        json.dump(product, file, indent=4, default=str)  # Convert datetime to string

    # Return the file as a response
    return FileResponse(
        path=file_path,
        filename=f"product_{product_id}.json",
        media_type="application/json"
    )