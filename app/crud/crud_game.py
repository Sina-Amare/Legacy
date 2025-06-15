from sqlalchemy.orm import Session, joinedload
from app.models.dynasty import Dynasty
from app.models.game import Game
from app.models.decision_option import DecisionOption
from app.schemas.game import GameCreate
from app.schemas.decision import DecisionSubmit

def get_game(db: Session, game_id: int) -> Game | None:
    """
    Retrieves a single game session by its ID.

    It eagerly loads the related dynasty information using `joinedload`
    to prevent common lazy-loading issues and optimize database queries.
    """
    return db.query(Game).options(joinedload(Game.dynasty)).filter(Game.id == game_id).first()


def create_game_session(db: Session, *, game_in: GameCreate) -> Game:
    """
    Creates a new game session and sets its initial state.

    The initial state is derived from the chosen dynasty's unique
    historical starting resources and its designated starting decision node.
    """
    dynasty = db.get(Dynasty, game_in.dynasty_id)
    if not dynasty:
        raise ValueError(f"Dynasty with id {game_in.dynasty_id} not found.")

    # Get starting resources from the dynasty's definition, with sensible fallbacks.
    initial = dynasty.initial_resources or {}
    new_game = Game(
        dynasty_id=game_in.dynasty_id,
        current_year=dynasty.start_year,
        current_decision_node_id=dynasty.start_decision_node_id,
        treasury=initial.get("treasury", 1000),
        stability=initial.get("stability", 70),
        military_strength=initial.get("military_strength", 100),
        religious_influence=initial.get("religious_influence", 50)
    )
    db.add(new_game)
    db.commit()
    db.refresh(new_game)
    return new_game


def process_player_decision(db: Session, *, game: Game, decision_in: DecisionSubmit) -> Game:
    """
    Processes a player's decision using a dynamic effects system.

    This function validates the choice, applies all defined effects
    (e.g., 'add', 'set') to the game's resources, advances the game
    to the next decision node, and increments the game year.

    Raises:
        ValueError: If the chosen option is invalid for the current decision.
    """
    option = db.get(DecisionOption, decision_in.option_id)

    if not option or option.node_id != game.current_decision_node_id:
        raise ValueError("Invalid option selected for the current decision.")

    if option.effects:
        for resource, effect in option.effects.items():
            if hasattr(game, resource):
                current_value = getattr(game, resource)
                operation = effect.get("operation", "add")  # Default to 'add'
                value = effect.get("value", 0)

                if operation == "add":
                    setattr(game, resource, current_value + value)
                elif operation == "set":
                    setattr(game, resource, value)
                elif operation == "multiply":
                    setattr(game, resource, int(current_value * value))
    
    game.current_decision_node_id = option.next_node_id
    game.current_year += 1  # Advance time by one year after each decision

    db.add(game)
    db.commit()
    db.refresh(game)
    return game
