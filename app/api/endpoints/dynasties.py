from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.dynasty import Dynasty as DynastySchema
from app.crud.crud_dynasty import get_dynasties, get_dynasty
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[DynastySchema])
def read_dynasties(db: Session = Depends(deps.get_db)) -> Any:
    """Retrieve all dynasties."""
    return get_dynasties(db=db)

@router.get("/{dynasty_id}", response_model=DynastySchema)
def read_dynasty_by_id(
    dynasty_id: int, db: Session = Depends(deps.get_db)
) -> Any:
    """Retrieve a specific dynasty by its ID."""
    dynasty = get_dynasty(db=db, dynasty_id=dynasty_id)
    if not dynasty:
        raise HTTPException(status_code=404, detail="Dynasty not found")
    return dynasty