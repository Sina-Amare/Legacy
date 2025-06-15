from pydantic import BaseModel
from .dynasty import Dynasty as DynastySchema

class GameBase(BaseModel):
    """Base properties for a game session."""
    dynasty_id: int

class GameCreate(GameBase):
    """Properties received via API for creating a new game."""
    pass

class Game(GameBase):
    """
    Properties to return to the client, now including the last narrative.
    """
    id: int
    current_year: int
    treasury: int
    stability: int
    military_strength: int
    religious_influence: int
    current_decision_node_id: int | None = None
    dynasty: DynastySchema
    
    # New field exposed in the API response.
    last_narrative: str | None = None

    class Config:
        from_attributes = True