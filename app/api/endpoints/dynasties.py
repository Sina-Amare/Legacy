# app/api/endpoints/dynasties.py
from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas, crud
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Dynasty]) # Corrected access
def read_dynasties(
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Retrieve all dynasties from the database.
    """
    dynasties = crud.get_dynasties(db=db)
    return dynasties