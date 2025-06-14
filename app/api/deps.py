# app/api/deps.py
from app.db.session import SessionLocal

def get_db():
    """
    Dependency function that provides a database session for each request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()