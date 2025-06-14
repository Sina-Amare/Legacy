from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base

class Game(Base):
    """
    Represents a single, ongoing game session in the database.

    Each instance tracks the state of a user's playthrough for a 
    specific dynasty, including their current resources and progress.
    """
    __tablename__ = 'games'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Foreign key to link this game session to a specific dynasty
    dynasty_id: Mapped[int] = mapped_column(Integer, ForeignKey("dynasties.id"))

    # The current year in the game's timeline, initialized to the dynasty's start
    current_year: Mapped[int] = mapped_column(Integer, nullable=False)

    # Core resources for the player's kingdom
    treasury: Mapped[int] = mapped_column(Integer, default=1000)
    stability: Mapped[int] = mapped_column(Integer, default=70) # Represented as a percentage
    military_strength: Mapped[int] = mapped_column(Integer, default=100)
    religious_influence: Mapped[int] = mapped_column(Integer, default=50)

    # Establishes a relationship to the Dynasty model for easy data access
    dynasty = relationship("Dynasty")