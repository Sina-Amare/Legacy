from pydantic import BaseModel
from typing import Any

class Dynasty(BaseModel):
    """Pydantic schema for returning dynasty data via the API."""
    id: int
    name: str
    country: str
    start_year: int
    end_year: int
    description: str | None = None
    image_url: str | None = None
    opening_brief: str | None = None
    start_decision_node_id: int | None = None
    
    # Expose initial resources to the API if needed in the future
    initial_resources: dict[str, Any] | None = None

    class Config:
        from_attributes = True