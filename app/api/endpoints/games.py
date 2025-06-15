from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from app.schemas.game import Game as GameSchema, GameCreate
from app.schemas.decision import DecisionSubmit
from app.crud.crud_game import create_game_session, get_game, trigger_decision_processing
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



@router.post("/{game_id}/decide", status_code=status.HTTP_202_ACCEPTED)
def submit_decision(
    *,
    game_id: int,
    db: Session = Depends(deps.get_db),
    decision_in: DecisionSubmit,
) -> Response:
    """
    Receives a player's decision and triggers the background task.
    Returns an empty 202 Accepted response immediately.
    """
    game = get_game(db=db, game_id=game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    try:
        trigger_decision_processing(db=db, game=game, decision_in=decision_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return Response(status_code=status.HTTP_202_ACCEPTED)