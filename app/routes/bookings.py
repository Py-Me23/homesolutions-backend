# app/routes/bookings.py

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from bson.objectid import ObjectId
from datetime import datetime
from app.database import bookings_collection, services_collection
from app.auth import authenticated_user
from app.authz import has_roles
from app.utils import replace_mongo_id

router = APIRouter()

class BookingCreateModel(BaseModel):
    service_id: str
    service_date: datetime
    notes: Optional[str]

class BookingUpdateModel(BaseModel):
    service_date: Optional[datetime]
    notes: Optional[str]
    status: Optional[str]  # pending, confirmed, completed, canceled

# Homeowner: create booking
@router.post("/", dependencies=[Depends(has_roles(["homeowner"]))])
async def create_booking(booking: BookingCreateModel, user=Depends(authenticated_user)):
    service = await services_collection.find_one({"_id": ObjectId(booking.service_id)})
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    if booking.service_date < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Service date must be in the future")

    doc = booking.dict()
    doc["homeowner_id"] = user["id"]
    doc["provider_id"] = None  # assigned later
    doc["status"] = "pending"
    doc["created_at"] = datetime.utcnow()

    result = await bookings_collection.insert_one(doc)
    doc["id"] = str(result.inserted_id)
    return replace_mongo_id(doc)

# Provider: view assigned bookings
@router.get("/assigned", dependencies=[Depends(has_roles(["provider"]))])
async def get_assigned_bookings(user=Depends(authenticated_user)):
    bookings = await bookings_collection.find({"provider_id": user["id"]}).to_list(length=100)
    return replace_mongo_id(bookings)

# Homeowner: view own bookings
@router.get("/my-bookings", dependencies=[Depends(has_roles(["homeowner"]))])
async def get_user_bookings(user=Depends(authenticated_user)):
    bookings = await bookings_collection.find({"homeowner_id": user["id"]}).to_list(length=100)
    return replace_mongo_id(bookings)

# Admin: get all bookings
@router.get("/", dependencies=[Depends(has_roles(["admin"]))])
async def get_all_bookings():
    bookings = await bookings_collection.find({}).to_list(length=200)
    return replace_mongo_id(bookings)
