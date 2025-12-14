# app/routes/users.py

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from app.auth import authenticated_user
from app.authz import has_roles
from app.database import users_collection
from app.utils import replace_mongo_id
from bson.objectid import ObjectId
import bcrypt
import jwt
import os
from datetime import datetime, timedelta

router = APIRouter()

# ----------------------------
# Pydantic models
# ----------------------------
class UserRegisterModel(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str  # "homeowner" or "provider"

class UserUpdateModel(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    services: Optional[List[str]] = None  # only for providers
    phone: Optional[List[str]] = []
    location: Optional[str] = None

class UserLoginModel(BaseModel):
    email: EmailStr
    password: str

# ----------------------------
# JWT helper
# ----------------------------
def create_jwt(user_id: str, role: str) -> str:
    payload = {
        "id": user_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=24)  # token valid for 24h
    }
    token = jwt.encode(payload, os.getenv("JWT_SECRET_KEY"), algorithm="HS256")
    return token

# ----------------------------
# User registration
# ----------------------------
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserRegisterModel):
    existing = await users_collection.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()
    user_dict = user.dict()
    user_dict["password"] = hashed_pw
    user_dict["created_at"] = datetime.utcnow()

    result = await users_collection.insert_one(user_dict)
    user_dict["id"] = str(result.inserted_id)
    return replace_mongo_id(user_dict)

# ----------------------------
# User login
# ----------------------------
@router.post("/login")
async def login(payload: UserLoginModel):
    user = await users_collection.find_one({"email": payload.email})
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Verify password
    if not bcrypt.checkpw(payload.password.encode("utf-8"), user["password"].encode("utf-8")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_jwt(str(user["_id"]), user.get("role", "user"))
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": replace_mongo_id(user)
    }

# ----------------------------
# Get own profile
# ----------------------------
@router.get("/me")
async def get_profile(user=Depends(authenticated_user)):
    return user

# ----------------------------
# Update own profile
# ----------------------------
@router.put("/me")
async def update_profile(update: UserUpdateModel, user=Depends(authenticated_user)):
    update_data = {k: v for k, v in update.dict().items() if v is not None}
    if "password" in update_data:
        update_data["password"] = bcrypt.hashpw(update_data["password"].encode(), bcrypt.gensalt()).decode()
    if update_data:
        await users_collection.update_one({"_id": ObjectId(user["id"])}, {"$set": update_data})
    updated_user = await users_collection.find_one({"_id": ObjectId(user["id"])})
    return replace_mongo_id(updated_user)

# ----------------------------
# Admin: get all users
# ----------------------------
@router.get("/", dependencies=[Depends(has_roles(["admin"]))])
async def get_all_users():
    users = await users_collection.find({}).to_list(length=100)
    return replace_mongo_id(users)
