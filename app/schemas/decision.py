from pydantic import BaseModel

class DecisionSubmit(BaseModel):
    """
    Represents the data received from the client when they make a decision.
    It contains the ID of the chosen option.
    """
    option_id: int