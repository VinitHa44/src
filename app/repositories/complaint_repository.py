from app.config.database import db
from app.models.domain.complaint import Complaint
from bson import ObjectId

class ComplaintRepository:
    @staticmethod
    async def create_complaint(complaint: Complaint):
        complaint_dict = complaint.__dict__
        result = await db.db["complaints"].insert_one(complaint_dict)
        return str(result.inserted_id)

 