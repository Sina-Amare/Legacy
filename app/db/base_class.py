# app/db/base_class.py
from sqlalchemy.orm import declarative_base

# A central declarative base for all SQLAlchemy ORM models.
Base = declarative_base()