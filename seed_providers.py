"""
Script to seed the database with providers for all categories.
Run this script to populate providers in the database.
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
import bcrypt
from datetime import datetime

load_dotenv()

MONGO_URL = os.getenv(
    "MONGO_URL",
    "mongodb+srv://homesolutions:home_solutions@grow-cohort6.nlxoztk.mongodb.net/"
)

# Providers for all categories
PROVIDERS = [
    # Plumbing
    {
        "name": "John Smith",
        "email": "john@smithplumbing.com",
        "password": bcrypt.hashpw("password123".encode(), bcrypt.gensalt()).decode(),
        "role": "provider",
        "businessName": "Smith Plumbing Solutions",
        "category": "Plumbing",
        "description": "Expert plumber with 15 years of experience in leak detection and pipe repair.",
        "location": "Downtown District",
        "coordinates": {"lat": 40.7128, "lng": -74.0060},
        "phone": "+1 (555) 012-3456",
        "imageUrl": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=200&auto=format&fit=crop",
        "portfolioImages": [
            "https://images.unsplash.com/photo-1581244277943-fe4a9c777189?q=80&w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1607472586893-edb57bdc0e39?q=80&w=800&auto=format&fit=crop"
        ],
        "isAvailable": True,
        "hourlyRate": 85.0,
        "rating": 4.8,
        "reviewCount": 124,
        "created_at": datetime.utcnow()
    },
    {
        "name": "Mike Johnson",
        "email": "mike@quickfixplumbing.com",
        "password": bcrypt.hashpw("password123".encode(), bcrypt.gensalt()).decode(),
        "role": "provider",
        "businessName": "Quick Fix Plumbing",
        "category": "Plumbing",
        "description": "24/7 emergency plumbing services. Fast response time and quality work guaranteed.",
        "location": "East Side",
        "coordinates": {"lat": 40.7300, "lng": -73.9800},
        "phone": "+1 (555) 234-5678",
        "imageUrl": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?q=80&w=200&auto=format&fit=crop",
        "portfolioImages": [],
        "isAvailable": True,
        "hourlyRate": 75.0,
        "rating": 4.6,
        "reviewCount": 89,
        "created_at": datetime.utcnow()
    },
    # Cleaning
    {
        "name": "Sarah Jenkins",
        "email": "sarah@sparkleclean.com",
        "password": bcrypt.hashpw("password123".encode(), bcrypt.gensalt()).decode(),
        "role": "provider",
        "businessName": "Sparkle Cleaners",
        "category": "Cleaning",
        "description": "Professional home cleaning services. We use eco-friendly products.",
        "location": "Westside Suburbs",
        "coordinates": {"lat": 40.7300, "lng": -74.0500},
        "phone": "+1 (555) 098-7654",
        "imageUrl": "https://images.unsplash.com/photo-1554151228-14d9def656ec?q=80&w=200&auto=format&fit=crop",
        "portfolioImages": [
            "https://images.unsplash.com/photo-1581578731117-104f2a863a30?q=80&w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1527515664-6277754394b0?q=80&w=800&auto=format&fit=crop"
        ],
        "isAvailable": True,
        "hourlyRate": 40.0,
        "rating": 4.9,
        "reviewCount": 89,
        "created_at": datetime.utcnow()
    },
    {
        "name": "Maria Garcia",
        "email": "maria@cleanteam.com",
        "password": bcrypt.hashpw("password123".encode(), bcrypt.gensalt()).decode(),
        "role": "provider",
        "businessName": "Clean Team Services",
        "category": "Cleaning",
        "description": "Thorough deep cleaning and regular maintenance. Licensed and insured.",
        "location": "North Hills",
        "coordinates": {"lat": 40.7500, "lng": -73.9700},
        "phone": "+1 (555) 345-6789",
        "imageUrl": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?q=80&w=200&auto=format&fit=crop",
        "portfolioImages": [],
        "isAvailable": True,
        "hourlyRate": 45.0,
        "rating": 4.7,
        "reviewCount": 67,
        "created_at": datetime.utcnow()
    },
    # Electrical
    {
        "name": "Mike Ross",
        "email": "mike@voltelectric.com",
        "password": bcrypt.hashpw("password123".encode(), bcrypt.gensalt()).decode(),
        "role": "provider",
        "businessName": "Volt Electric",
        "category": "Electrical",
        "description": "Licensed electrician specializing in home wiring and smart home setups.",
        "location": "North Hills",
        "coordinates": {"lat": 40.7500, "lng": -73.9800},
        "phone": "+1 (555) 111-2222",
        "imageUrl": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?q=80&w=200&auto=format&fit=crop",
        "portfolioImages": [
            "https://images.unsplash.com/photo-1621905251189-08b45d6a269e?q=80&w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1558402091-7688501235b0?q=80&w=800&auto=format&fit=crop"
        ],
        "isAvailable": False,
        "hourlyRate": 95.0,
        "rating": 4.7,
        "reviewCount": 56,
        "created_at": datetime.utcnow()
    },
    {
        "name": "David Chen",
        "email": "david@brightelectric.com",
        "password": bcrypt.hashpw("password123".encode(), bcrypt.gensalt()).decode(),
        "role": "provider",
        "businessName": "Bright Electric Solutions",
        "category": "Electrical",
        "description": "Expert electrical repairs and installations. Safety first approach.",
        "location": "South Park",
        "coordinates": {"lat": 40.7000, "lng": -74.0100},
        "phone": "+1 (555) 456-7890",
        "imageUrl": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?q=80&w=200&auto=format&fit=crop",
        "portfolioImages": [],
        "isAvailable": True,
        "hourlyRate": 90.0,
        "rating": 4.9,
        "reviewCount": 112,
        "created_at": datetime.utcnow()
    },
    # Painting
    {
        "name": "Emma Stone",
        "email": "emma@colorworld.com",
        "password": bcrypt.hashpw("password123".encode(), bcrypt.gensalt()).decode(),
        "role": "provider",
        "businessName": "Color World Painting",
        "category": "Painting",
        "description": "Interior and exterior painting. High attention to detail.",
        "location": "East Village",
        "coordinates": {"lat": 40.7200, "lng": -73.9900},
        "phone": "+1 (555) 333-4444",
        "imageUrl": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?q=80&w=200&auto=format&fit=crop",
        "portfolioImages": [
            "https://images.unsplash.com/photo-1589939705384-5185137a7f0f?q=80&w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1562259949-e8e7689d7828?q=80&w=800&auto=format&fit=crop"
        ],
        "isAvailable": True,
        "hourlyRate": 60.0,
        "rating": 4.6,
        "reviewCount": 42,
        "created_at": datetime.utcnow()
    },
    {
        "name": "Robert Martinez",
        "email": "robert@premiumpaint.com",
        "password": bcrypt.hashpw("password123".encode(), bcrypt.gensalt()).decode(),
        "role": "provider",
        "businessName": "Premium Paint Co",
        "category": "Painting",
        "description": "Professional painting services for homes and businesses. Quality paints and expert application.",
        "location": "Uptown",
        "coordinates": {"lat": 40.7800, "lng": -73.9600},
        "phone": "+1 (555) 567-8901",
        "imageUrl": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?q=80&w=200&auto=format&fit=crop",
        "portfolioImages": [],
        "isAvailable": True,
        "hourlyRate": 65.0,
        "rating": 4.8,
        "reviewCount": 78,
        "created_at": datetime.utcnow()
    },
    # Carpentry
    {
        "name": "David Wood",
        "email": "dave@woodworks.com",
        "password": bcrypt.hashpw("password123".encode(), bcrypt.gensalt()).decode(),
        "role": "provider",
        "businessName": "WoodWorks Carpentry",
        "category": "Carpentry",
        "description": "Custom furniture and cabinet repairs.",
        "location": "Uptown",
        "coordinates": {"lat": 40.7800, "lng": -73.9600},
        "phone": "+1 (555) 555-6666",
        "imageUrl": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?q=80&w=200&auto=format&fit=crop",
        "portfolioImages": [
            "https://images.unsplash.com/photo-1611244419377-b0a760c19719?q=80&w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1533090161767-e6ffed986c88?q=80&w=800&auto=format&fit=crop"
        ],
        "isAvailable": True,
        "hourlyRate": 75.0,
        "rating": 4.9,
        "reviewCount": 15,
        "created_at": datetime.utcnow()
    },
    {
        "name": "James Carpenter",
        "email": "james@mastercraft.com",
        "password": bcrypt.hashpw("password123".encode(), bcrypt.gensalt()).decode(),
        "role": "provider",
        "businessName": "MasterCraft Carpentry",
        "category": "Carpentry",
        "description": "Expert carpentry services including custom builds, repairs, and installations.",
        "location": "Midtown",
        "coordinates": {"lat": 40.7500, "lng": -73.9900},
        "phone": "+1 (555) 678-9012",
        "imageUrl": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=200&auto=format&fit=crop",
        "portfolioImages": [],
        "isAvailable": True,
        "hourlyRate": 80.0,
        "rating": 4.7,
        "reviewCount": 34,
        "created_at": datetime.utcnow()
    },
    # Gardening
    {
        "name": "Linda Green",
        "email": "linda@greenthumb.com",
        "password": bcrypt.hashpw("password123".encode(), bcrypt.gensalt()).decode(),
        "role": "provider",
        "businessName": "Green Thumb Gardening",
        "category": "Gardening",
        "description": "Landscaping, lawn maintenance, and garden design.",
        "location": "Suburbs",
        "coordinates": {"lat": 40.8000, "lng": -74.1000},
        "phone": "+1 (555) 777-8888",
        "imageUrl": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?q=80&w=200&auto=format&fit=crop",
        "portfolioImages": [
            "https://images.unsplash.com/photo-1558904541-efa843a96f01?q=80&w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?q=80&w=800&auto=format&fit=crop"
        ],
        "isAvailable": True,
        "hourlyRate": 50.0,
        "rating": 4.5,
        "reviewCount": 30,
        "created_at": datetime.utcnow()
    },
    # Moving
    {
        "name": "Tom Wilson",
        "email": "tom@quickmove.com",
        "password": bcrypt.hashpw("password123".encode(), bcrypt.gensalt()).decode(),
        "role": "provider",
        "businessName": "Quick Move Services",
        "category": "Moving",
        "description": "Professional moving services with experienced team. Careful handling guaranteed.",
        "location": "Central District",
        "coordinates": {"lat": 40.7500, "lng": -74.0000},
        "phone": "+1 (555) 789-0123",
        "imageUrl": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=200&auto=format&fit=crop",
        "portfolioImages": [],
        "isAvailable": True,
        "hourlyRate": 100.0,
        "rating": 4.8,
        "reviewCount": 45,
        "created_at": datetime.utcnow()
    },
    # Decorating
    {
        "name": "Sophie Anderson",
        "email": "sophie@styledesign.com",
        "password": bcrypt.hashpw("password123".encode(), bcrypt.gensalt()).decode(),
        "role": "provider",
        "businessName": "Style Design Interiors",
        "category": "Decorating",
        "description": "Interior design and decoration services. Transform your space with style.",
        "location": "Design District",
        "coordinates": {"lat": 40.7600, "lng": -73.9700},
        "phone": "+1 (555) 890-1234",
        "imageUrl": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?q=80&w=200&auto=format&fit=crop",
        "portfolioImages": [],
        "isAvailable": True,
        "hourlyRate": 120.0,
        "rating": 4.9,
        "reviewCount": 28,
        "created_at": datetime.utcnow()
    },
    # Additional providers for better coverage
    # Plumbing - 3rd provider
    {
        "name": "Alex Rivera",
        "email": "alex@riveraplumbing.com",
        "password": bcrypt.hashpw("password123".encode(), bcrypt.gensalt()).decode(),
        "role": "provider",
        "businessName": "Rivera Plumbing Experts",
        "category": "Plumbing",
        "description": "Licensed master plumber specializing in residential and commercial plumbing. Emergency services available 24/7.",
        "location": "Southside",
        "coordinates": {"lat": 40.7000, "lng": -74.0200},
        "phone": "+1 (555) 901-2345",
        "imageUrl": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?q=80&w=400&auto=format&fit=crop",
        "portfolioImages": [],
        "isAvailable": True,
        "hourlyRate": 90.0,
        "rating": 4.7,
        "reviewCount": 67,
        "created_at": datetime.utcnow()
    },
    # Cleaning - 3rd provider
    {
        "name": "Jennifer White",
        "email": "jennifer@sparklepro.com",
        "password": bcrypt.hashpw("password123".encode(), bcrypt.gensalt()).decode(),
        "role": "provider",
        "businessName": "Sparkle Pro Cleaning",
        "category": "Cleaning",
        "description": "Professional cleaning services for homes and offices. Deep cleaning, regular maintenance, and move-in/out services.",
        "location": "West End",
        "coordinates": {"lat": 40.7400, "lng": -74.0600},
        "phone": "+1 (555) 012-3457",
        "imageUrl": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?q=80&w=400&auto=format&fit=crop",
        "portfolioImages": [],
        "isAvailable": True,
        "hourlyRate": 42.0,
        "rating": 4.8,
        "reviewCount": 95,
        "created_at": datetime.utcnow()
    },
    # Electrical - 3rd provider
    {
        "name": "Kevin Park",
        "email": "kevin@powerup.com",
        "password": bcrypt.hashpw("password123".encode(), bcrypt.gensalt()).decode(),
        "role": "provider",
        "businessName": "PowerUp Electrical",
        "category": "Electrical",
        "description": "Certified electrician with expertise in residential wiring, panel upgrades, and electrical troubleshooting.",
        "location": "Riverside",
        "coordinates": {"lat": 40.7200, "lng": -74.0300},
        "phone": "+1 (555) 234-5679",
        "imageUrl": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=400&auto=format&fit=crop",
        "portfolioImages": [],
        "isAvailable": True,
        "hourlyRate": 88.0,
        "rating": 4.6,
        "reviewCount": 52,
        "created_at": datetime.utcnow()
    },
    # Painting - 3rd provider
    {
        "name": "Lisa Brown",
        "email": "lisa@freshcoat.com",
        "password": bcrypt.hashpw("password123".encode(), bcrypt.gensalt()).decode(),
        "role": "provider",
        "businessName": "Fresh Coat Painting",
        "category": "Painting",
        "description": "Professional painting services with premium paints. Interior, exterior, and specialty finishes available.",
        "location": "Park District",
        "coordinates": {"lat": 40.7700, "lng": -73.9500},
        "phone": "+1 (555) 345-6780",
        "imageUrl": "https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?q=80&w=400&auto=format&fit=crop",
        "portfolioImages": [],
        "isAvailable": True,
        "hourlyRate": 58.0,
        "rating": 4.9,
        "reviewCount": 88,
        "created_at": datetime.utcnow()
    },
    # Carpentry - 3rd provider
    {
        "name": "Carlos Mendez",
        "email": "carlos@finewood.com",
        "password": bcrypt.hashpw("password123".encode(), bcrypt.gensalt()).decode(),
        "role": "provider",
        "businessName": "Fine Wood Carpentry",
        "category": "Carpentry",
        "description": "Master carpenter specializing in custom furniture, built-ins, and fine woodworking. Precision and quality guaranteed.",
        "location": "Artisan Quarter",
        "coordinates": {"lat": 40.7600, "lng": -73.9400},
        "phone": "+1 (555) 456-7891",
        "imageUrl": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=400&auto=format&fit=crop",
        "portfolioImages": [],
        "isAvailable": True,
        "hourlyRate": 85.0,
        "rating": 5.0,
        "reviewCount": 41,
        "created_at": datetime.utcnow()
    },
    # Gardening - 2nd provider
    {
        "name": "Robert Green",
        "email": "robert@landscapedesign.com",
        "password": bcrypt.hashpw("password123".encode(), bcrypt.gensalt()).decode(),
        "role": "provider",
        "businessName": "Landscape Design Pro",
        "category": "Gardening",
        "description": "Professional landscaping and garden design. Lawn care, planting, and outdoor space transformation.",
        "location": "Garden District",
        "coordinates": {"lat": 40.7900, "lng": -74.0900},
        "phone": "+1 (555) 567-8902",
        "imageUrl": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=400&auto=format&fit=crop",
        "portfolioImages": [],
        "isAvailable": True,
        "hourlyRate": 55.0,
        "rating": 4.8,
        "reviewCount": 73,
        "created_at": datetime.utcnow()
    },
    # Moving - 2nd provider
    {
        "name": "Steve Thompson",
        "email": "steve@reliablemovers.com",
        "password": bcrypt.hashpw("password123".encode(), bcrypt.gensalt()).decode(),
        "role": "provider",
        "businessName": "Reliable Movers",
        "category": "Moving",
        "description": "Experienced moving team with full-service packing and transportation. Licensed and insured.",
        "location": "Transport Hub",
        "coordinates": {"lat": 40.7300, "lng": -74.0100},
        "phone": "+1 (555) 678-9013",
        "imageUrl": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=400&auto=format&fit=crop",
        "portfolioImages": [],
        "isAvailable": True,
        "hourlyRate": 95.0,
        "rating": 4.7,
        "reviewCount": 56,
        "created_at": datetime.utcnow()
    },
    # Decorating - 2nd provider
    {
        "name": "Amanda Taylor",
        "email": "amanda@elegantspaces.com",
        "password": bcrypt.hashpw("password123".encode(), bcrypt.gensalt()).decode(),
        "role": "provider",
        "businessName": "Elegant Spaces Design",
        "category": "Decorating",
        "description": "Interior design and home staging services. Creating beautiful, functional spaces tailored to your style.",
        "location": "Fashion District",
        "coordinates": {"lat": 40.7500, "lng": -73.9800},
        "phone": "+1 (555) 789-0124",
        "imageUrl": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?q=80&w=400&auto=format&fit=crop",
        "portfolioImages": [],
        "isAvailable": True,
        "hourlyRate": 125.0,
        "rating": 4.9,
        "reviewCount": 62,
        "created_at": datetime.utcnow()
    },
]

async def seed_providers():
    """Seed the users collection with providers for all categories."""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client["homesolutions"]
    users_collection = db["users"]
    
    print("Starting to seed providers...")
    
    # Check if providers already exist
    existing_count = await users_collection.count_documents({"role": "provider"})
    if existing_count > 0:
        print(f"Found {existing_count} existing providers.")
        print("Adding new providers (skipping duplicates)...")
    
    # Insert providers
    inserted_count = 0
    for provider in PROVIDERS:
        # Check if email already exists
        existing = await users_collection.find_one({"email": provider["email"]})
        if existing:
            print(f"  - Skipping {provider['businessName']} (email already exists)")
            continue
        
        result = await users_collection.insert_one(provider)
        inserted_count += 1
        print(f"  - Added {provider['businessName']} ({provider['category']})")
    
    print(f"\nSuccessfully inserted {inserted_count} providers!")
    print(f"Total providers in database: {await users_collection.count_documents({'role': 'provider'})}")
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_providers())

