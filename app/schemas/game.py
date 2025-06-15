from pydantic import BaseModel
from typing import Any, Dict
from .dynasty import Dynasty as DynastySchema

class GameBase(BaseModel):
    """Base properties for a game session."""
    dynasty_id: int

class GameCreate(GameBase):
    """Properties received via API for creating a new game."""
    pass

class Game(GameBase):
    """
    Schema for returning the full game state to the client,
    including the dynamically generated story and options.
    """
    id: int
    current_year: int
    treasury: int
    stability: int
    military_strength: int
    religious_influence: int
    dynasty: DynastySchema
    
    current_story_text: str | None = None
    current_options: Dict[str, str] | None = None
    last_narrative: str | None = None

    class Config:
        from_attributes = True