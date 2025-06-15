# app/api/endpoints/decisions.py
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
# Direct imports for schemas and models
from app.schemas.decision_node import DecisionNode as DecisionNodeSchema
from app.models.decision_node import DecisionNode

router = APIRouter()

@router.get("/{node_id}", response_model=DecisionNodeSchema)
def get_decision_node(
    node_id: int,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Retrieve a specific decision node and its options by ID.
    """
    decision_node = db.get(DecisionNode, node_id) # Using the modern db.get()
    if not decision_node:
        raise HTTPException(status_code=404, detail="Decision node not found")
    return decision_node