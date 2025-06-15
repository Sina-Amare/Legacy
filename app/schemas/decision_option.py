from pydantic import BaseModel
from typing import Any

class DecisionOption(BaseModel):
    """Pydantic schema for a single decision option."""
    id: int
    option_text: str
    effects: dict[str, Any] | None = None

    class Config:
        from_attributes = True