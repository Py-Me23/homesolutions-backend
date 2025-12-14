import os
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.database import users_collection
from app.utils import replace_mongo_id
from bson.objectid import ObjectId
import jwt
from datetime import datetime, timedelta
import bcrypt
from pydantic import BaseModel, EmailStr, Field

# JWT Authentication
security = HTTPBearer()

# Pydantic models
class RegisterModel(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: str = Field(..., pattern="^(homeowner|provider)$")

class LoginModel(BaseModel):
    email: EmailStr
    password: str

# JWT helper
def create_jwt(user_id: str) -> str:
    payload = {
        "id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    token = jwt.encode(payload, os.getenv("JWT_SECRET_KEY"), algorithm="HS256")
    return token

# Authentication dependency
async def authenticated_user(
    auth: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        payload = jwt.decode(auth.credentials, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
        user_id = payload["id"]
        user = await users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return replace_mongo_id(user)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
