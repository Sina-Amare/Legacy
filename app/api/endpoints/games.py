from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.game import Game as GameSchema, GameCreate
from app.schemas.decision import DecisionSubmit
from app.crud.crud_game import create_game_session, get_game, process_player_decision
from app.api import deps

router = APIRouter()

@router.get("/{game_id}", response_model=GameSchema)
def read_game_by_id(game_id: int, db: Session = Depends(deps.get_db)) -> Any:
    """Retrieve a specific game session by its ID."""
    game = get_game(db=db, game_id=game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game

@router.post("/", response_model=GameSchema)
def create_new_game(*, db: Session = Depends(deps.get_db), game_in: GameCreate) -> Any:
    """Create a new game session for a chosen dynasty."""
    try:
        game = create_game_session(db=db, game_in=game_in)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return game

@router.post("/{game_id}/decide", response_model=GameSchema)
def submit_decision(
    *,
    game_id: int,
    db: Session = Depends(deps.get_db),
    decision_in: DecisionSubmit,
) -> Any:
    """
    Submit a player's decision for a given game and process the consequences.
    This is the core endpoint for gameplay interaction.
    """
    game = get_game(db=db, game_id=game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    try:
        updated_game = process_player_decision(db=db, game=game, decision_in=decision_in)
    except ValueError as e:
        # A 400 Bad Request is suitable for an invalid player action
        raise HTTPException(status_code=400, detail=str(e))

    return updated_game