import json
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.core.config import settings
from app.schemas.game import Game as GameSchema

def get_llm():
    """Initializes and returns the language model instance with secure API key handling."""
    return ChatOpenAI(
        model=settings.OPENROUTER_MODEL_NAME,
        api_key=settings.OPENROUTER_API_KEY, # Pass the SecretStr object directly
        base_url=settings.OPENROUTER_API_BASE,
        temperature=0.8,
        model_kwargs={"max_tokens": 1024}
    )

def generate_initial_story_and_options(dynasty_name: str, opening_brief: str) -> dict:
    """Generates the very first decision point for a new game using an AI."""
    llm = get_llm()
    template = """
    You are the Game Master for a historical simulation game named 'Legacy'.
    The player has chosen to play as the '{dynasty_name}'.
    The historical context is: {opening_brief}

    Your task is to generate the very first decision point.
    1.  Create a compelling narrative text ('story_text') describing the initial situation.
    2.  Create exactly four strategic, distinct options ('options') for the player.
    3.  The options must be a dictionary with keys "1", "2", "3", "4".

    Your entire response MUST be a single, valid JSON object with two keys: "story_text" and "options".
    Example: {{"story_text": "...", "options": {{"1": "...", "2": "...", "3": "...", "4": "..."}}}}
    """
    
    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm | StrOutputParser()
    
    try:
        raw_response = chain.invoke({"dynasty_name": dynasty_name, "opening_brief": opening_brief})
        if "```json" in raw_response:
            raw_response = raw_response.split("```json")[1].split("```")[0].strip()
        return json.loads(raw_response)
    except (json.JSONDecodeError, Exception) as e:
        print(f"AI initial story generation failed: {e}")
        return {"story_text": "خطا در خلق داستان اولیه. لطفا دوباره تلاش کنید.", "options": {}}

def generate_next_story(game_state: GameSchema, player_choice: str) -> dict:
    """
    Generates the next game state based on the player's last choice.
    """
    llm = get_llm()
    game_state_dict = game_state.model_dump()
    template = """
    You are a master storyteller and strategic Game Master for the game 'Legacy'.
    The current state of the player's kingdom is: {game_state}
    The player just made the following decision: '{player_choice}'

    Your task is to generate the next turn of the game.
    1.  **Calculate Effects:** Based on the player's choice, determine the numerical effects. This should be a dictionary ('effects') with keys 'treasury', 'stability', 'military_strength', 'religious_influence' and integer values (e.g., -100, 20).
    2.  **Narrate the Outcome:** Write a compelling, historical narrative ('narrative') that explains the consequences. Explain *why* the resources changed in a story-driven way.
    3.  **Create the Next Situation:** Based on the new reality, create a new situation for the player to face ('story_text').
    4.  **Generate New Options:** Provide four new, distinct strategic options ('options') for this new situation.

    Your entire response MUST be a single, valid JSON object with four keys: "narrative", "effects", "story_text", and "options".
    """

    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm | StrOutputParser()

    try:
        raw_response = chain.invoke({
            "game_state": json.dumps(game_state_dict, ensure_ascii=False),
            "player_choice": player_choice
        })
        if "```json" in raw_response:
            raw_response = raw_response.split("```json")[1].split("```")[0].strip()
        return json.loads(raw_response)
    except (json.JSONDecodeError, Exception) as e:
        print(f"AI next story generation failed: {e}")
        return {
            "narrative": "وقایع‌نگار از ثبت ادامه این سرگذشت بازمانده است.",
            "effects": {}, "story_text": "تاریخ در این نقطه به سکوت می‌رسد.", "options": {}
        }