# app/routes/payments.py

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List
from bson.objectid import ObjectId
from datetime import datetime
from app.database import payments_collection, bookings_collection
from app.auth import authenticated_user
from app.authz import has_roles
from app.utils import replace_mongo_id

router = APIRouter()

class PaymentCreateModel(BaseModel):
    booking_id: str
    amount: float = Field(..., gt=0)
    payment_method: str

# Homeowner: create payment
@router.post("/", dependencies=[Depends(has_roles(["homeowner"]))])
async def create_payment(payment: PaymentCreateModel, user=Depends(authenticated_user)):
    booking = await bookings_collection.find_one({"_id": ObjectId(payment.booking_id)})
    if not booking or booking["homeowner_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Invalid booking")

    doc = payment.dict()
    doc["user_id"] = user["id"]
    doc["status"] = "pending"
    doc["created_at"] = datetime.utcnow()

    result = await payments_collection.insert_one(doc)
    doc["id"] = str(result.inserted_id)
    return replace_mongo_id(doc)

# Admin: get all payments
@router.get("/", dependencies=[Depends(has_roles(["admin"]))])
async def get_all_payments():
    payments = await payments_collection.find({}).to_list(length=200)
    return replace_mongo_id(payments)
