# app/routes/providers.py

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
from bson.objectid import ObjectId
from app.database import db
from app.authz import has_roles
from app.utils import replace_mongo_id
from datetime import datetime

router = APIRouter()

# Use db collections
providers_collection = db.providers

# Pydantic Schemas
class ProviderCreateModel(BaseModel):
    name: str = Field(..., min_length=2)
    service_type: str
    email: str
    phone: str
    description: Optional[str]

class ProviderUpdateModel(BaseModel):
    name: Optional[str]
    service_type: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    description: Optional[str]

# Create provider (admin only)
@router.post("/", dependencies=[Depends(has_roles(["admin"]))])
async def create_provider(provider: ProviderCreateModel):
    provider_doc = provider.dict()
    provider_doc["created_at"] = datetime.utcnow()
    result = await providers_collection.insert_one(provider_doc)
    provider_doc["id"] = str(result.inserted_id)
    return replace_mongo_id(provider_doc)

# Get all providers
@router.get("/", response_model=List[dict])
async def get_providers():
    cursor = providers_collection.find({})
    providers = await cursor.to_list(length=100)
    return replace_mongo_id(providers)

# Get single provider
@router.get("/{provider_id}")
async def get_provider(provider_id: str):
    provider = await providers_collection.find_one({"_id": ObjectId(provider_id)})
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return replace_mongo_id(provider)

# Update provider (admin only)
@router.put("/{provider_id}", dependencies=[Depends(has_roles(["admin"]))])
async def update_provider(provider_id: str, update: ProviderUpdateModel):
    update_data = {k: v for k, v in update.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    result = await providers_collection.update_one(
        {"_id": ObjectId(provider_id)}, {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Provider not found")
    updated_provider = await providers_collection.find_one({"_id": ObjectId(provider_id)})
    return replace_mongo_id(updated_provider)

# Delete provider (admin only)
@router.delete("/{provider_id}", dependencies=[Depends(has_roles(["admin"]))])
async def delete_provider(provider_id: str):
    result = await providers_collection.delete_one({"_id": ObjectId(provider_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Provider not found")
    return {"message": "Provider deleted successfully"}
