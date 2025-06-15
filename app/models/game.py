from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base

class Game(Base):
    """
    Represents a single, ongoing game session in the database.
    Default values are removed, as they will be set dynamically on creation.
    """
    __tablename__ = 'games'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    dynasty_id: Mapped[int] = mapped_column(Integer, ForeignKey("dynasties.id"))
    current_decision_node_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("decision_nodes.id", name="fk_game_decision_node"), nullable=True
    )

    current_year: Mapped[int]
    treasury: Mapped[int]
    stability: Mapped[int]
    military_strength: Mapped[int]
    religious_influence: Mapped[int]

    dynasty = relationship("Dynasty")