from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class Dynasty(Base):
    """
    Represents a historical dynasty, including its unique starting conditions.
    """
    __tablename__ = 'dynasties'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    start_year: Mapped[int] = mapped_column(Integer, nullable=False)
    end_year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    image_url: Mapped[str | None] = mapped_column(String, nullable=True)
    opening_brief: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    start_decision_node_id: Mapped[int | None] = mapped_column(
        Integer, 
        ForeignKey("decision_nodes.id", name="fk_dynasty_start_node"), 
        nullable=True
    )

    # This new field stores the unique starting resources for this dynasty.
    initial_resources: Mapped[dict | None] = mapped_column(JSON, nullable=True)