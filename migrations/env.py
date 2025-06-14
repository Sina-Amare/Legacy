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
# This allows Alembic to find our application modules (like app.core.config).
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import our application's settings and the Base model for SQLAlchemy.
# `settings` holds our database URL.
# `Base` is the declarative base from which all our models inherit.
from app.core.config import settings
from app.db.base_class import Base
from app.models import * # Import all models to ensure they are registered with Base.metadata

# --- Standard Alembic Configuration ---

# This is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Set the database URL from our central settings file.
# This ensures that Alembic and our FastAPI app always use the same database.
config.set_main_option('sqlalchemy.url', settings.DATABASE_URL)


# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- Target Metadata Setup for Autogenerate ---

# This is the most important part for the 'autogenerate' feature.
# We are telling Alembic that our SQLAlchemy models (registered with Base.metadata)
# represent the target state of our database schema.
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
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
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Get the configuration section from the .ini file
    configuration = config.get_section(config.config_ini_section)

    # Ensure the configuration is not None before proceeding
    if configuration is not None:
        # Set the database URL from our central settings object
        configuration["sqlalchemy.url"] = settings.DATABASE_URL
        
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