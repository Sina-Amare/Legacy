from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base

class Dynasty(Base):
    __tablename__ = 'dynasties'
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    start_year: Mapped[int] = mapped_column(Integer, nullable=False)
    end_year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    image_url: Mapped[str | None] = mapped_column(String, nullable=True)
    # New field for the opening brief
    opening_brief: Mapped[str | None] = mapped_column(Text, nullable=True)