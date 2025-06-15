# scripts/create_tables.py
from app.db.base_class import Base
from app.db.session import engine

# Import all models so that they are registered with the Base metadata
from app.models import *

def main() -> None:
    """
    A simple script to create all database tables based on SQLAlchemy models.

    This script connects to the database using the engine and issues
    CREATE TABLE statements for all tables that do not yet exist.
    """
    print("Connecting to the database and creating tables...")
    try:
        # The create_all method checks for the existence of tables before creating them.
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully (if they didn't already exist).")
    except Exception as e:
        print(f"An error occurred during table creation: {e}")

if __name__ == "__main__":
    main()