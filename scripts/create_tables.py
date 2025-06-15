from app.db.base_class import Base
from app.db.session import engine
from app.models import *

def main() -> None:
    """A script to create all database tables based on SQLAlchemy models."""
    print("Connecting to the database to create tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully (if they didn't already exist).")
    except Exception as e:
        print(f"An error occurred during table creation: {e}")

if __name__ == "__main__":
    main()