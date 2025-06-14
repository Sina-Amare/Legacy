from sqlalchemy.orm import Session
from app.models.dynasty import Dynasty
from app.models.game import Game
from app.schemas.game import GameCreate

def create_game_session(db: Session, *, game_in: GameCreate) -> Game:
    """
    Creates a new game session based on a chosen dynasty.

    Args:
        db: The SQLAlchemy database session.
        game_in: The input data, containing the dynasty_id.

    Raises:
        ValueError: If the dynasty with the given ID does not exist.

    Returns:
        The newly created Game object.
    """
    dynasty = db.query(Dynasty).filter(Dynasty.id == game_in.dynasty_id).first()
    if not dynasty:
        raise ValueError(f"Dynasty with id {game_in.dynasty_id} not found.")

    new_game = Game(
        dynasty_id=game_in.dynasty_id,
        current_year=dynasty.start_year
    )
    db.add(new_game)
    db.commit()
    db.refresh(new_game)
    return new_game