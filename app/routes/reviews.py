# app/routes/reviews.py

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List
from bson.objectid import ObjectId
from datetime import datetime
from app.database import reviews_collection, users_collection
from app.auth import authenticated_user
from app.authz import has_roles
from app.utils import replace_mongo_id

router = APIRouter()

class ReviewCreateModel(BaseModel):
    provider_id: str
    rating: int = Field(..., ge=1, le=5)
    comment: str

# Create review (homeowner only)
@router.post("/", dependencies=[Depends(lambda: has_roles(["homeowner"]))])
async def create_review(review: ReviewCreateModel, user=Depends(authenticated_user)):
    provider = await users_collection.find_one({"_id": ObjectId(review.provider_id), "role": "provider"})
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    doc = review.dict()
    doc["homeowner_id"] = user["id"]
    doc["created_at"] = datetime.utcnow()

    result = await reviews_collection.insert_one(doc)
    doc["id"] = str(result.inserted_id)
    return replace_mongo_id(doc)

# Provider: view own reviews
@router.get("/my-reviews", dependencies=[Depends(lambda: has_roles(["provider"]))])
async def get_my_reviews(user=Depends(authenticated_user)):
    reviews = await reviews_collection.find({"provider_id": user["id"]}).to_list(length=100)
    return replace_mongo_id(reviews)
