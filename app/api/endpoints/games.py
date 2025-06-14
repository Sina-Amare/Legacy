from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.game import Game as GameSchema, GameCreate
from app.crud.crud_game import create_game_session
from app.api import deps

router = APIRouter()

@router.post("/", response_model=GameSchema)
def create_new_game(
    *,
    db: Session = Depends(deps.get_db),
    game_in: GameCreate,
) -> Any:
    """Create a new game session for a chosen dynasty."""
    try:
        game = create_game_session(db=db, game_in=game_in)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return game