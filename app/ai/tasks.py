import asyncio
from app.celery_app import celery_app
from app.ai.game_master import generate_next_story
from app.db.session import SessionLocal
from app.models.game import Game
from app.schemas.game import Game as GameSchema
from app.ws.manager import manager

@celery_app.task
def process_decision_task(game_id: int, player_choice_text: str):
    """
    A Celery task that calls the AI Game Master, updates the database,
    and notifies the client via WebSocket with the full new game state.
    """
    print(f"Celery Task: Processing decision for game {game_id}...")
    db = SessionLocal()
    try:
        game = db.get(Game, game_id)
        if not game:
            return

        game_schema = GameSchema.model_validate(game)
        ai_result = generate_next_story(game_schema, player_choice_text)

        game.last_narrative = ai_result.get("narrative")
        game.current_story_text = ai_result.get("story_text")
        game.current_options = ai_result.get("options")
        
        effects = ai_result.get("effects", {})
        for resource, value in effects.items():
            if hasattr(game, resource):
                current_value = getattr(game, resource)
                setattr(game, resource, current_value + value)
        
        game.current_year += 1
        db.commit()
        db.refresh(game)
        
        print(f"Celery Task: Game {game_id} updated in DB.")
        
        # Notify client with the complete new game state
        updated_game_data = GameSchema.model_validate(game).model_dump()
        asyncio.run(manager.send_json_message(updated_game_data, game_id))
        print(f"Celery Task: WebSocket notification sent for game {game_id}.")

    except Exception as e:
        print(f"Celery Task Error: {e}")
        db.rollback()
    finally:
        db.close()