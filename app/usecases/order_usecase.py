from typing import List
from app.repositories.order_repository import OrderRepository
from app.models.domain.order import Order, OrderItem
from app.models.schemas.order_schema import OrderSchema

def objectid_to_str(order):
    order['_id'] = str(order['_id'])  # Convert ObjectId to string
    order['user_id'] = str(order['user_id'])  # Convert ObjectId to string
    for item in order['items']:
        item['product_id'] = str(item['product_id'])  # Convert ObjectId to string for each product_id
    return order

class OrderUseCase:

    @staticmethod
    async def place_order(user_id: str, cart_items: List[dict]):
        order_items = []
        for item in cart_items:  
            order_items.append(OrderItem(
                product_id=str(item["product_id"]),
                quantity=item["quantity"],
                price=item["price"]  # Use the price from updated_cart_items
            ))

        if not order_items:
            return {"error": "Cart is empty"}

        # Calculate total price (assuming price is fetched later)
        total_amount = sum(item.quantity * item.price for item in order_items)

        order = Order(
            user_id=user_id,
            items=order_items,
            total_amount=total_amount,
            status="delivered"
        )

        order_id = await OrderRepository.create_order(order)
        return {"message": "Order placed successfully", "order_id": order_id}
    
    @staticmethod
    async def get_orders(user_id: str):
        orders = await OrderRepository.get_orders_by_user(user_id)
        return [objectid_to_str(order) for order in orders]

    @staticmethod
    async def get_order_details(order_id: str):
        order = await OrderRepository.get_order_by_id(order_id)
        if not order:
            return {"error": "Order not found"}
        return objectid_to_str(order)
