# app/models/decision_node.py

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class DecisionNode(Base):
    """
    Represents a single decision point (a node) in the story tree.
    """
    __tablename__ = 'decision_nodes'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    node_text: Mapped[str]

    # This relationship defines the list of choices available at this node.
    # We explicitly provide `foreign_keys` to resolve the ambiguity caused
    # by having multiple foreign keys to the same table in DecisionOption.
    options = relationship(
        "DecisionOption",
        # This tells SQLAlchemy to use the 'node_id' column on the DecisionOption
        # model to find all options belonging to this DecisionNode.
        foreign_keys="DecisionOption.node_id",
        back_populates="node"
    )