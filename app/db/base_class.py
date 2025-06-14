# app/db/base_class.py
from sqlalchemy.orm import declarative_base

# A central declarative base for all SQLAlchemy ORM models.
# All data models in the application will inherit from this Base class.
# This allows Alembic to discover the models and manage migrations.
Base = declarative_base()