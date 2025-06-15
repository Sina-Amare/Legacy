from pydantic import BaseModel
from .dynasty import Dynasty as DynastySchema # Import the dynasty schema

class GameBase(BaseModel):
    """Base properties for a game session."""
    dynasty_id: int

class GameCreate(GameBase):
    """Properties received via API for creating a new game."""
    pass

class Game(GameBase):
    """
    Properties to return to the client via API.
    This now includes the full related Dynasty object.
    """
    id: int
    current_year: int
    treasury: int
    stability: int
    military_strength: int
    religious_influence: int
    current_decision_node_id: int | None = None

    # This tells Pydantic to expect a nested Dynasty object in the response
    dynasty: DynastySchema

    class Config:
        from_attributes = True
