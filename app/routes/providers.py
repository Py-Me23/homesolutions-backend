# app/routes/providers.py

from fastapi import APIRouter, HTTPException
from typing import List
from bson.objectid import ObjectId
from app.database import users_collection, reviews_collection
from app.utils import replace_mongo_id

router = APIRouter()

# Get all providers
@router.get("/", response_model=List[dict])
async def get_providers():
    """
    Get all providers (users with role='provider').
    Transforms user data to match frontend Provider interface.
    """
    providers = await users_collection.find({"role": "provider"}).to_list(length=100)
    
    result = []
    for provider in providers:
        provider_dict = replace_mongo_id(provider)
        
        # Get reviews for this provider
        reviews = await reviews_collection.find({"provider_id": provider_dict["id"]}).to_list(length=100)
        reviews_list = replace_mongo_id(reviews)
        
        # Calculate rating and review count
        # Use stored rating if available, otherwise calculate from reviews
        rating = provider_dict.get("rating", 0.0)
        review_count = provider_dict.get("reviewCount", len(reviews_list))
        if review_count == 0 and len(reviews_list) > 0:
            total_rating = sum(r.get("rating", 0) for r in reviews_list)
            rating = round(total_rating / len(reviews_list), 1)
            review_count = len(reviews_list)
        
        # Transform to match frontend Provider interface
        # Map backend fields to frontend fields
        provider_data = {
            "id": provider_dict.get("id", ""),
            "name": provider_dict.get("name", ""),
            "businessName": provider_dict.get("businessName") or provider_dict.get("name", ""),
            "category": provider_dict.get("category") or provider_dict.get("services", [""])[0] if provider_dict.get("services") else "Other",
            "description": provider_dict.get("description") or provider_dict.get("bio") or "Professional service provider",
            "location": provider_dict.get("location") or "Not specified",
            "coordinates": provider_dict.get("coordinates") or {"lat": 0.0, "lng": 0.0},
            "phone": (provider_dict.get("phone", [""])[0] if isinstance(provider_dict.get("phone"), list) else provider_dict.get("phone") or ""),
            "email": provider_dict.get("email", ""),
            "rating": rating,
            "reviewCount": review_count,
            "reviews": [
                {
                    "id": r.get("id", ""),
                    "userId": r.get("homeowner_id", ""),
                    "userName": r.get("userName") or "Anonymous",
                    "rating": r.get("rating", 0),
                    "comment": r.get("comment", ""),
                    "date": r.get("created_at", "").isoformat() if r.get("created_at") else ""
                }
                for r in reviews_list
            ],
            "imageUrl": provider_dict.get("imageUrl") or provider_dict.get("avatar") or "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=200&auto=format&fit=crop",
            "portfolioImages": provider_dict.get("portfolioImages") or [],
            "isAvailable": provider_dict.get("isAvailable", True),
            "hourlyRate": provider_dict.get("hourlyRate") or provider_dict.get("rate") or 50.0
        }
        result.append(provider_data)
    
    return result

# Get single provider by ID
@router.get("/{provider_id}")
async def get_provider(provider_id: str):
    """
    Get a single provider by ID.
    """
    try:
        provider = await users_collection.find_one({"_id": ObjectId(provider_id), "role": "provider"})
        if not provider:
            raise HTTPException(status_code=404, detail="Provider not found")
        
        provider_dict = replace_mongo_id(provider)
        
        # Get reviews for this provider
        reviews = await reviews_collection.find({"provider_id": provider_dict["id"]}).to_list(length=100)
        reviews_list = replace_mongo_id(reviews)
        
        # Calculate rating and review count
        # Use stored rating if available, otherwise calculate from reviews
        rating = provider_dict.get("rating", 0.0)
        review_count = provider_dict.get("reviewCount", len(reviews_list))
        if review_count == 0 and len(reviews_list) > 0:
            total_rating = sum(r.get("rating", 0) for r in reviews_list)
            rating = round(total_rating / len(reviews_list), 1)
            review_count = len(reviews_list)
        
        # Transform to match frontend Provider interface
        provider_data = {
            "id": provider_dict.get("id", ""),
            "name": provider_dict.get("name", ""),
            "businessName": provider_dict.get("businessName") or provider_dict.get("name", ""),
            "category": provider_dict.get("category") or provider_dict.get("services", [""])[0] if provider_dict.get("services") else "Other",
            "description": provider_dict.get("description") or provider_dict.get("bio") or "Professional service provider",
            "location": provider_dict.get("location") or "Not specified",
            "coordinates": provider_dict.get("coordinates") or {"lat": 0.0, "lng": 0.0},
            "phone": (provider_dict.get("phone", [""])[0] if isinstance(provider_dict.get("phone"), list) else provider_dict.get("phone") or ""),
            "email": provider_dict.get("email", ""),
            "rating": rating,
            "reviewCount": review_count,
            "reviews": [
                {
                    "id": r.get("id", ""),
                    "userId": r.get("homeowner_id", ""),
                    "userName": r.get("userName") or "Anonymous",
                    "rating": r.get("rating", 0),
                    "comment": r.get("comment", ""),
                    "date": r.get("created_at", "").isoformat() if r.get("created_at") else ""
                }
                for r in reviews_list
            ],
            "imageUrl": provider_dict.get("imageUrl") or provider_dict.get("avatar") or "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=200&auto=format&fit=crop",
            "portfolioImages": provider_dict.get("portfolioImages") or [],
            "isAvailable": provider_dict.get("isAvailable", True),
            "hourlyRate": provider_dict.get("hourlyRate") or provider_dict.get("rate") or 50.0
        }
        
        return provider_data
    except Exception as e:
        if "not a valid ObjectId" in str(e):
            raise HTTPException(status_code=400, detail="Invalid provider ID")
        raise HTTPException(status_code=500, detail=str(e))

