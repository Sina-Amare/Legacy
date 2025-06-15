from app.db.session import SessionLocal

def get_db():
    """
    FastAPI Dependency to create and manage a database session per request.

    This function uses a 'yield' statement, which ensures that the database
    session is always closed after the request is finished, even if an

    error occurs. This is the standard, robust way to handle sessions in FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()