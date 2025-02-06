from datetime import datetime
import random
from typing import Optional
from fastapi import HTTPException, UploadFile
import httpx
import requests
from app.models.schemas.product_schema import ProductCreateSchema
from app.repositories.product_repository import ProductRepository
from app.models.domain.product import Product
from bson import ObjectId

from app.utils.gd_utils import upload_to_google_drive

class ProductUseCase:
    DUMMYJSON_URL = "https://dummyjson.com/products"

    @staticmethod
    async def preload_products(predefined_seller_ids: list):
        async with httpx.AsyncClient() as client:
            response = await client.get(ProductUseCase.DUMMYJSON_URL)
            products = response.json().get("products", [])

        for product in products:
            random_seller_id = random.choice(predefined_seller_ids)
            new_product = Product(
                title=product["title"],
                description=product["description"],
                category=product["category"],
                price=product["price"],
                rating=product["rating"],
                brand=product.get("brand", "Unknown"),
                images=product["images"],
                thumbnail=product["thumbnail"],
                seller_id=random_seller_id
            )
            await ProductRepository.insert_product(new_product.__dict__)

        return {"message": f"{len(products)} products preloaded successfully"}
    
    @staticmethod
    async def create_product(product_data: dict, file: UploadFile, seller_id: str):
        try:
            validated_data = ProductCreateSchema(**product_data)  # Validate input

            file_drive = await upload_to_google_drive(file)
            file_url = f"https://drive.google.com/file/d/{file_drive['id']}/view"

            validated_data_dict = validated_data.dict()
            validated_data_dict["images"] = [file_url]
            validated_data_dict["seller_id"] = ObjectId(seller_id)

            product = Product(**validated_data_dict)
            created_product = await ProductRepository.create_product(product)

            if not created_product:
                return {"error": "Failed to create product"}

            return created_product

        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    @staticmethod
    async def get_all_products():
        products = await ProductRepository.get_all_products()
        return products
    
    @staticmethod
    async def get_product_by_id(product_id: str):
        product = await ProductRepository.get_product_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    @staticmethod
    async def delete_product(product_id: str, user: dict):
        product = await ProductRepository.get_product_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        # Only allow admin or product's seller to delete
        if user["role"] != "admin" and product["seller_id"] != user["id"]:
            raise HTTPException(status_code=403, detail="Permission denied")

        success = await ProductRepository.delete_product(product_id)
        if success:
            return {"message": "Product deleted successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to delete product")
        
    @staticmethod
    async def update_product(product_id: str, product_data: dict, file: UploadFile, seller_id: str):
        try:
            validated_data = ProductCreateSchema(**product_data)  # Validate input

            validated_data_dict = validated_data.dict()
            if file:
                file_drive = await upload_to_google_drive(file)
                validated_data_dict["images"] = [f"https://drive.google.com/file/d/{file_drive['id']}/view"]

            return await ProductRepository.update_product(product_id, validated_data_dict, seller_id)
        
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

