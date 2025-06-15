from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base

class Game(Base):
    """
    Represents a single, ongoing game session in the database.

    This model tracks the state of a user's playthrough for a specific dynasty,
    including their current resources, progress, and the current decision they face.
    """
    __tablename__ = 'games'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # Foreign key to link this game session to a specific dynasty.
    dynasty_id: Mapped[int] = mapped_column(Integer, ForeignKey("dynasties.id"))

    # Tracks the current decision node the player is facing.
    # This will be updated as the player makes choices.
    current_decision_node_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("decision_nodes.id", name="fk_game_decision_node"), nullable=True
    )

    # The current year in the game's timeline.
    current_year: Mapped[int]
    
    # Core resources for the player's kingdom.
    treasury: Mapped[int] = mapped_column(Integer, default=1000)
    stability: Mapped[int] = mapped_column(Integer, default=70) # Represented as a percentage
    military_strength: Mapped[int] = mapped_column(Integer, default=100)
    religious_influence: Mapped[int] = mapped_column(Integer, default=50)

    # Establishes a relationship to the Dynasty model for easy data access.
    dynasty = relationship("Dynasty")