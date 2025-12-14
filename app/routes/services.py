# app/routes/services.py

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
from bson.objectid import ObjectId
from datetime import datetime
from app.database import services_collection
from app.authz import has_roles
from app.utils import replace_mongo_id

router = APIRouter()

class ServiceCreateModel(BaseModel):
    name: str = Field(..., min_length=2)
    category: str
    description: Optional[str] = None
    price: float = Field(..., gt=0)

class ServiceUpdateModel(BaseModel):
    name: Optional[str]
    category: Optional[str]
    description: Optional[str]
    price: Optional[float]

# Admin: create service
@router.post("/", dependencies=[Depends(has_roles(["admin"]))])
async def create_service(service: ServiceCreateModel):
    doc = service.dict()
    doc["created_at"] = datetime.utcnow()
    result = await services_collection.insert_one(doc)
    doc["id"] = str(result.inserted_id)
    return replace_mongo_id(doc)

# Get all services
@router.get("/", response_model=List[dict])
async def get_services():
    services = await services_collection.find({}).to_list(length=100)
    return replace_mongo_id(services)

# Get single service
@router.get("/{service_id}")
async def get_service(service_id: str):
    service = await services_collection.find_one({"_id": ObjectId(service_id)})
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return replace_mongo_id(service)

# Admin: update service
@router.put("/{service_id}", dependencies=[Depends(has_roles(["admin"]))])
async def update_service(service_id: str, update: ServiceUpdateModel):
    data = {k: v for k, v in update.dict().items() if v is not None}
    if not data:
        raise HTTPException(status_code=400, detail="No fields to update")
    await services_collection.update_one({"_id": ObjectId(service_id)}, {"$set": data})
    updated = await services_collection.find_one({"_id": ObjectId(service_id)})
    return replace_mongo_id(updated)

# Admin: delete service
@router.delete("/{service_id}", dependencies=[Depends(has_roles(["admin"]))])
async def delete_service(service_id: str):
    result = await services_collection.delete_one({"_id": ObjectId(service_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Service not found")
    return {"message": "Service deleted successfully"}
