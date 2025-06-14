# scripts/seed.py
import asyncio
from app.db.session import SessionLocal
from app.models.dynasty import Dynasty

# Initial data for the dynasties table
initial_dynasties = [
    {
        "name": "Achaemenid Empire",
        "country": "Persia",
        "start_year": -550,
        "end_year": -330,
        "description": "The first Persian Empire, founded by Cyrus the Great."
    },
    {
        "name": "Sasanian Empire",
        "country": "Persia",
        "start_year": 224,
        "end_year": 651,
        "description": "The last Persian imperial dynasty before the Muslim conquest."
    }
]

async def seed_data():
    print("Seeding initial data...")
    db = SessionLocal()
    try:
        for dynasty_data in initial_dynasties:
            # Check if dynasty already exists
            existing_dynasty = db.query(Dynasty).filter(Dynasty.name == dynasty_data["name"]).first()
            if not existing_dynasty:
                db.add(Dynasty(**dynasty_data))
        db.commit()
        print("Data seeded successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(seed_data())