from sqlalchemy.orm import Session
from app.models.dynasty import Dynasty

def get_dynasties(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve all dynasty records, sorted by their start year.
    """
    return db.query(Dynasty).order_by(Dynasty.start_year.asc()).offset(skip).limit(limit).all()

def get_dynasty(db: Session, dynasty_id: int):
    """
    Retrieve a single dynasty by its unique ID.
    """
    return db.query(Dynasty).filter(Dynasty.id == dynasty_id).first()