# migrations/env.py
import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# --- Project Specific Setup ---
# This block is crucial for connecting Alembic to our FastAPI application.

# Add the project's root directory to the Python path.
# This allows Alembic to find our application modules.
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

# Import our application's settings and the Base model for SQLAlchemy.
from app.core.config import settings
from app.db.base_class import Base
from app.models import * # This ensures all models are registered with Base.metadata

# --- Standard Alembic Configuration ---

config = context.config

# Set the database URL from our central settings file.
if settings.DATABASE_URL:
    config.set_main_option('sqlalchemy.url', settings.DATABASE_URL)
else:
    raise ValueError("DATABASE_URL is not set in the environment variables.")

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- Target Metadata Setup for Autogenerate ---
# This tells Alembic what our SQLAlchemy models' state should be.
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    configuration = config.get_section(config.config_ini_section)
    if configuration:
        connectable = engine_from_config(
            configuration,
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )
        with connectable.connect() as connection:
            context.configure(
                connection=connection, target_metadata=target_metadata
            )
            with context.begin_transaction():
                context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
