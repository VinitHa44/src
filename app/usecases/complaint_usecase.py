from app.repositories.complaint_repository import ComplaintRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.user_repository import UserRepository
from app.utils.email_utils import send_complaint_email
from app.models.domain.complaint import Complaint
from bson import ObjectId

class ComplaintUseCase:
    @staticmethod
    async def file_complaint(data):
        complaint = Complaint(
            user_id=ObjectId(data.user_id),
            order_id=ObjectId(data.order_id),
            product_id=ObjectId(data.product_id),
            issue=data.issue,
            image_url=data.image_url
        )
        
        # Store the complaint in the database
        complaint_id = await ComplaintRepository.create_complaint(complaint)

        # Fetch the seller ID from the product
        seller_id = await ProductRepository.get_seller_id(data.product_id)
        if not seller_id:
            raise ValueError("Seller ID not found for this product")

        # Fetch the seller email
        seller_email = await UserRepository.get_user_email(seller_id)
        if not seller_email:
            raise ValueError("Seller email not found")

        # Send the complaint email to seller and admin
        send_complaint_email(complaint, seller_email)

        return {"message": "Complaint submitted successfully", "complaint_id": complaint_id}
