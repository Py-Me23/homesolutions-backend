
# app/database.py

from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB connection URL
MONGO_URL = os.getenv(
    "MONGO_URL",
    "mongodb+srv://homesolutions:home_solutions@grow-cohort6.nlxoztk.mongodb.net/"
)

# Create async MongoDB client
client = AsyncIOMotorClient(MONGO_URL)

# Access the database
homesolutions_db = client["homesolutions"]

# Define collections
services_collection = homesolutions_db["services"]      # Available services
users_collection = homesolutions_db["users"]            # User accounts
bookings_collection = homesolutions_db["bookings"]      # Service bookings
reviews_collection = homesolutions_db["reviews"]        # Optional: user reviews
payments_collection = homesolutions_db["payments"]      # Optional: payment records

# Example helper function to test connection
async def test_db_connection():
    try:
        # The "ping" command checks the connection
        await homesolutions_db.command("ping")
        print("MongoDB connection successful!")
    except Exception as e:
        print("MongoDB connection failed:", e)
