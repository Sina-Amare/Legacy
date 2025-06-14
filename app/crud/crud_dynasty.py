# app/crud/crud_dynasty.py
from sqlalchemy.orm import Session
from app.models.dynasty import Dynasty

def get_dynasties(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Dynasty).offset(skip).limit(limit).all()