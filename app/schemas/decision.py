from pydantic import BaseModel

class DecisionSubmit(BaseModel):
    """
    Represents the data payload received from the client when they make a decision.
    It contains the key of the chosen option (e.g., "1", "2", "3", "4").
    """
    option_key: str