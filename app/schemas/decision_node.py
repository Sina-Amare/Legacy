from pydantic import BaseModel
from typing import List
from .decision_option import DecisionOption

class DecisionNode(BaseModel):
    """Pydantic schema for a decision node, including its available options."""
    id: int
    node_text: str
    options: List[DecisionOption] = []

    class Config:
        from_attributes = True