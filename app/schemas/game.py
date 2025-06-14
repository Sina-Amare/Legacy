from pydantic import BaseModel

class GameBase(BaseModel):
    """Base properties for a game session."""
    dynasty_id: int

class GameCreate(GameBase):
    """Properties received via API for creating a new game."""
    pass

class Game(GameBase):
    """Properties to return to the client via API."""
    id: int
    current_year: int
    treasury: int
    stability: int
    military_strength: int
    religious_influence: int

    class Config:
        # Enables mapping from SQLAlchemy models to Pydantic schemas
        from_attributes = True