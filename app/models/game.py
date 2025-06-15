from sqlalchemy import Column, Integer, ForeignKey, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base

class Game(Base):
    """
    Represents a single, ongoing game session in the database.
    This model is the source of truth for a player's current state,
    which is updated dynamically by the AI Game Master.
    """
    __tablename__ = 'games'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    dynasty_id: Mapped[int] = mapped_column(Integer, ForeignKey("dynasties.id"))

    # Stores the last generated narrative text OR the current decision prompt.
    current_story_text: Mapped[str | None] = mapped_column(Text)
    
    # Stores the dynamically generated options for the current state as a JSON object.
    # e.g., {"1": "Option A Text", "2": "Option B Text", ...}
    current_options: Mapped[dict | None] = mapped_column(JSON)
    
    # The current year in the game's timeline.
    current_year: Mapped[int]
    
    # Core resources for the player's kingdom.
    treasury: Mapped[int]
    stability: Mapped[int]
    military_strength: Mapped[int]
    religious_influence: Mapped[int]
    
    # This field is used to display the narrative result of a decision.
    last_narrative: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Establishes a relationship to the Dynasty model for easy data access.
    dynasty = relationship("Dynasty")