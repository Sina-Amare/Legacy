from app.worker import celery_app
from app.ai.narrator import get_narrative_for_outcome
from app.db.session import SessionLocal
from app.models.game import Game
from app.ws.manager import manager

@celery_app.task
def generate_narrative_task(game_id: int, context_for_ai: str):
    """
    A Celery task that generates a narrative in the background,
    updates the database, and notifies the client via WebSocket.
    """
    print(f"Celery Task: Generating narrative for game {game_id}...")
    narrative = get_narrative_for_outcome(context_for_ai)
    
    db = SessionLocal()
    try:
        # Fetch the game session from the database
        game = db.get(Game, game_id)
        if game:
            # Update the game record with the new narrative
            game.last_narrative = narrative
            db.add(game)
            db.commit()
            print(f"Celery Task: Narrative saved to DB for game {game_id}.")
            
            # Notify the client that the new narrative is ready
            # This is a simplified approach for a single-server setup.
            import asyncio
            asyncio.run(manager.send_personal_message(f"NARRATIVE_READY:{narrative}", game_id))
            print(f"Celery Task: WebSocket notification sent for game {game_id}.")

    except Exception as e:
        print(f"Celery Task Error: Failed to update game with narrative. {e}")
        db.rollback()
    finally:
        db.close()
    
    return narrative