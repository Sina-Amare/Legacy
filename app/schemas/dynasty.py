from pydantic import BaseModel

class Dynasty(BaseModel):
    id: int
    name: str
    country: str
    start_year: int
    end_year: int
    description: str | None = None
    image_url: str | None = None
    # New field for the API schema
    opening_brief: str | None = None

    class Config:
        from_attributes = True