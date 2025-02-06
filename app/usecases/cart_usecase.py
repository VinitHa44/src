from app.repositories.cart_repository import CartRepository

class CartUseCase:
    @staticmethod
    async def get_cart(user_id: str):
        return await CartRepository.get_cart(user_id)

    @staticmethod
    async def add_to_cart(user_id: str, items: list):
        if not items:
            return {"error": "Cart must contain at least one item"}
        
        for item in items:
            if item.quantity <= 0:
                return {"error": f"Invalid quantity {item.quantity} for product {item.product_id}"}

        return await CartRepository.add_to_cart(user_id, items)

    @staticmethod
    async def remove_from_cart(user_id: str, product_id: str):
        return await CartRepository.remove_from_cart(user_id, product_id)
