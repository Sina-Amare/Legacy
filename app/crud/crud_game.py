from sqlalchemy.orm import Session, joinedload
from app.models.dynasty import Dynasty
from app.models.game import Game
from app.models.decision_option import DecisionOption
from app.schemas.game import GameCreate
from app.schemas.decision import DecisionSubmit

def get_game(db: Session, game_id: int) -> Game | None:
    """
    Retrieves a single game session by its ID, eagerly loading the
    related dynasty information to prevent lazy-loading issues.
    """
    return db.query(Game).options(joinedload(Game.dynasty)).filter(Game.id == game_id).first()

def create_game_session(db: Session, *, game_in: GameCreate) -> Game:
    """Creates a new game session and sets its initial state."""
    dynasty = db.get(Dynasty, game_in.dynasty_id)
    if not dynasty:
        raise ValueError(f"Dynasty with id {game_in.dynasty_id} not found.")

    new_game = Game(
        dynasty_id=game_in.dynasty_id,
        current_year=dynasty.start_year,
        current_decision_node_id=dynasty.start_decision_node_id
    )
    db.add(new_game)
    db.commit()
    db.refresh(new_game)
    return new_game

def process_player_decision(db: Session, *, game: Game, decision_in: DecisionSubmit) -> Game:
    """
    Processes a player's decision, updates game state, and moves to the next node.
    """
    option = db.get(DecisionOption, decision_in.option_id)

    if not option or option.node_id != game.current_decision_node_id:
        raise ValueError("Invalid option selected for the current decision.")

    if option.effects:
        for resource, value in option.effects.items():
            if hasattr(game, resource):
                current_value = getattr(game, resource)
                setattr(game, resource, current_value + value)

    game.current_decision_node_id = option.next_node_id
    # We can advance time here as well, e.g., game.current_year += 1

    db.add(game)
    db.commit()
    db.refresh(game)
    return game
