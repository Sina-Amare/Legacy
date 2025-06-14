# app/schemas/dynasty.py
from pydantic import BaseModel

class Dynasty(BaseModel):
    id: int
    name: str
    country: str
    start_year: int
    end_year: int
    description: str | None = None

    class Config:
        from_attributes = True