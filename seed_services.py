"""
Script to seed the database with top 5 services.
Run this script to populate services in the database.
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv(
    "MONGO_URL",
    "mongodb+srv://homesolutions:home_solutions@grow-cohort6.nlxoztk.mongodb.net/"
)

# Top 5 services to seed
SERVICES = [
    {
        "name": "Plumbing Services",
        "category": "Plumbing",
        "description": "Expert plumbing services including leak repairs, pipe installation, drain cleaning, water heater services, and emergency plumbing.",
        "price": 85.0
    },
    {
        "name": "Painting Services",
        "category": "Painting",
        "description": "Professional interior and exterior painting services. We provide high-quality paint jobs for homes and businesses with attention to detail.",
        "price": 60.0
    },
    {
        "name": "Electrical Services",
        "category": "Electrical",
        "description": "Licensed electricians offering wiring, electrical repairs, panel upgrades, smart home installation, and electrical safety inspections.",
        "price": 95.0
    },
    {
        "name": "Home Cleaning Services",
        "category": "Cleaning",
        "description": "Thorough home cleaning services including deep cleaning, regular maintenance, move-in/move-out cleaning, and eco-friendly options.",
        "price": 40.0
    },
    {
        "name": "Carpentry Services",
        "category": "Carpentry",
        "description": "Skilled carpenters providing custom furniture, cabinet installation, repairs, woodworking, and general carpentry services.",
        "price": 75.0
    }
]

async def seed_services():
    """Seed the services collection with top 5 services."""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client["homesolutions"]
    services_collection = db["services"]
    
    print("Starting to seed services...")
    
    # Check if services already exist
    existing_count = await services_collection.count_documents({})
    if existing_count > 0:
        print(f"Found {existing_count} existing services. Skipping seed.")
        print("To re-seed, delete existing services first.")
        return
    
    # Insert services
    result = await services_collection.insert_many(SERVICES)
    print(f"Successfully inserted {len(result.inserted_ids)} services:")
    
    for service in SERVICES:
        print(f"  - {service['name']} ({service['category']}) - ${service['price']}/hr")
    
    print("\nServices seeded successfully!")
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_services())

