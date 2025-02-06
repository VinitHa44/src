from app.models.domain.user import User
from app.config.database import db
from bson import ObjectId

async def get_user_email(user_id: str):
    user = await db.db["users"].find_one({"_id": ObjectId(user_id)})
    if user:
        return user.get("email")
    return None
class UserRepository:
    @staticmethod
    async def get_user_by_email(email: str):
        return await db.db["users"].find_one({"email": email})

    @staticmethod
    async def create_user(user: User):
        user_dict = user.__dict__
        result = await db.db["users"].insert_one(user_dict)
        return str(result.inserted_id)
    
    @staticmethod
    async def get_user_email(user_id: str):
        user = await db.db["users"].find_one({"_id": ObjectId(user_id)})
        return user.get("email") if user else None
    
