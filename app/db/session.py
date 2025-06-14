# app/db/session.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Create the SQLAlchemy engine
# The engine is the entry point to the database.
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)


# Create a SessionLocal class
# Each instance of a SessionLocal will be a new database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)