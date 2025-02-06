from app.repositories.user_repository import UserRepository
from app.utils.auth_utils import hash_password, verify_password, create_access_token
from app.models.schemas.user_schema import UserCreate, UserLogin
from app.models.domain.user import User
from bson import ObjectId

class UserUseCase:
    @staticmethod
    async def register_user(user_data: UserCreate):
        existing_user = await UserRepository.get_user_by_email(user_data.email)
        if existing_user:
            return {"error": "Email already exists"}

        hashed_password = hash_password(user_data.password)
        user = User(
            name=user_data.name,
            email=user_data.email,
            password_hash=hashed_password,
            role=user_data.role
        )
        user_id = await UserRepository.create_user(user)
        return {"message": "User registered successfully", "user_id": user_id}

    @staticmethod
    async def login_user(user_data: UserLogin):
        user = await UserRepository.get_user_by_email(user_data.email)
        if not user or not verify_password(user_data.password, user["password_hash"]):
            return {"error": "Invalid credentials"}

        access_token = create_access_token({"sub": user["email"], "role": user["role"], "user_id": str(user["_id"])})
        return {"access_token": access_token, "token_type": "bearer"}
