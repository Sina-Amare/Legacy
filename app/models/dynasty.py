# app/models/dynasty.py
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class Dynasty(Base):
    """
    Represents a historical dynasty in the database using SQLAlchemy 2.0 syntax.
    """
    __tablename__ = 'dynasties'  # Explicitly defining the table name

    # The 'id' column is now defined using Mapped and mapped_column
    # Mapped[int] tells the type checker this column behaves like an integer.
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Other columns follow the same pattern
    name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    start_year: Mapped[int] = mapped_column(Integer, nullable=False)
    end_year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)

    # In the future, relationships to Rulers will be defined here.