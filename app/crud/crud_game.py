from sqlalchemy.orm import Session, joinedload
from app.models.dynasty import Dynasty
from app.models.game import Game
from app.schemas.game import GameCreate
from app.schemas.decision import DecisionSubmit
from app.ai.tasks import process_decision_task

def get_game(db: Session, game_id: int) -> Game | None:
    """Retrieves a single game session by its ID, eagerly loading dynasty info."""
    return db.query(Game).options(joinedload(Game.dynasty)).filter(Game.id == game_id).first()

def create_game_session(db: Session, *, game_in: GameCreate) -> Game:
    """
    Creates a new game session and uses the AI Game Master to generate
    the initial story and options dynamically.
    """
    dynasty = db.get(Dynasty, game_in.dynasty_id)
    if not dynasty:
        raise ValueError(f"Dynasty with id {game_in.dynasty_id} not found.")

    from app.ai.game_master import generate_initial_story_and_options
    initial_story = generate_initial_story_and_options(dynasty.name, dynasty.opening_brief or "")

    initial_resources = dynasty.initial_resources or {}
    
    new_game = Game(
        dynasty_id=dynasty.id,
        current_year=dynasty.start_year,
        current_story_text=initial_story.get("story_text"),
        current_options=initial_story.get("options"),
        treasury=initial_resources.get("treasury", 1000),
        stability=initial_resources.get("stability", 70),
        military_strength=initial_resources.get("military_strength", 100),
        religious_influence=initial_resources.get("religious_influence", 50),
        last_narrative=f"سرگذشت شما با {dynasty.name} آغاز می‌شود..."
    )
    db.add(new_game)
    db.commit()
    db.refresh(new_game)
    return new_game

def trigger_decision_processing(db: Session, *, game: Game, decision_in: DecisionSubmit):
    """
    Validates the player's choice and triggers the background processing task.
    This function no longer returns anything as the response is handled by Celery/WebSockets.
    """
    if not game.current_options:
        raise ValueError("No options available for this game state.")
        
    chosen_option_text = game.current_options.get(decision_in.option_key)
    if not chosen_option_text:
        raise ValueError("Invalid option key submitted.")

    # Trigger the Celery task to process everything in the background.
    process_decision_task.delay(game.id, chosen_option_text)