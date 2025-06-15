from pydantic import BaseModel

class DecisionSubmit(BaseModel):
    """
    Represents the data payload received from the client when they make a decision.
    It contains the unique identifier of the chosen option.
    """
    option_id: int