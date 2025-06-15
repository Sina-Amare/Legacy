from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class Dynasty(Base):
    """
    Represents a historical dynasty in the database.
    Each dynasty has a unique starting point in the decision tree.
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
    
    # This foreign key links the dynasty to its initial decision node.
    # We provide an explicit name for the constraint to ensure Alembic
    # can correctly manage upgrades and downgrades.
    start_decision_node_id: Mapped[int | None] = mapped_column(
        Integer, 
        ForeignKey("decision_nodes.id", name="fk_dynasty_start_node"), 
        nullable=True
    )