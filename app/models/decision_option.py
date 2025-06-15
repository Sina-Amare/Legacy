from sqlalchemy import Column, Integer, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base

class DecisionOption(Base):
    """Represents a single choice (an edge) leading from a decision node."""
    __tablename__ = 'decision_options'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    option_text: Mapped[str]

    # The node this option belongs to.
    node_id: Mapped[int] = mapped_column(Integer, ForeignKey("decision_nodes.id"))

    # The node this option leads to.
    next_node_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("decision_nodes.id"), nullable=True)

    # JSON field to store the effects of this choice on game resources.
    effects: Mapped[dict] = mapped_column(JSON, nullable=True) # e.g., {"stability": -10, "treasury": +200}

    node = relationship("DecisionNode", foreign_keys=[node_id], back_populates="options")