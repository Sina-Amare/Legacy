"""Create initial project schema

Revision ID: 50f61419d9ba
Revises: 
Create Date: 2025-06-15 23:10:47.959209

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '50f61419d9ba'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('decision_nodes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('node_text', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_decision_nodes_id'), 'decision_nodes', ['id'], unique=False)
    op.create_table('decision_options',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('option_text', sa.String(), nullable=False),
    sa.Column('node_id', sa.Integer(), nullable=False),
    sa.Column('next_node_id', sa.Integer(), nullable=True),
    sa.Column('effects', sa.JSON(), nullable=True),
    sa.ForeignKeyConstraint(['next_node_id'], ['decision_nodes.id'], ),
    sa.ForeignKeyConstraint(['node_id'], ['decision_nodes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_decision_options_id'), 'decision_options', ['id'], unique=False)
    op.create_table('dynasties',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('country', sa.String(length=100), nullable=False),
    sa.Column('start_year', sa.Integer(), nullable=False),
    sa.Column('end_year', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('image_url', sa.String(), nullable=True),
    sa.Column('opening_brief', sa.Text(), nullable=True),
    sa.Column('start_decision_node_id', sa.Integer(), nullable=True),
    sa.Column('initial_resources', sa.JSON(), nullable=True),
    sa.ForeignKeyConstraint(['start_decision_node_id'], ['decision_nodes.id'], name='fk_dynasty_start_node'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_dynasties_id'), 'dynasties', ['id'], unique=False)
    op.create_index(op.f('ix_dynasties_name'), 'dynasties', ['name'], unique=False)
    op.create_table('games',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('dynasty_id', sa.Integer(), nullable=False),
    sa.Column('current_story_text', sa.Text(), nullable=True),
    sa.Column('current_options', sa.JSON(), nullable=True),
    sa.Column('current_year', sa.Integer(), nullable=False),
    sa.Column('treasury', sa.Integer(), nullable=False),
    sa.Column('stability', sa.Integer(), nullable=False),
    sa.Column('military_strength', sa.Integer(), nullable=False),
    sa.Column('religious_influence', sa.Integer(), nullable=False),
    sa.Column('last_narrative', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['dynasty_id'], ['dynasties.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_games_id'), 'games', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_games_id'), table_name='games')
    op.drop_table('games')
    op.drop_index(op.f('ix_dynasties_name'), table_name='dynasties')
    op.drop_index(op.f('ix_dynasties_id'), table_name='dynasties')
    op.drop_table('dynasties')
    op.drop_index(op.f('ix_decision_options_id'), table_name='decision_options')
    op.drop_table('decision_options')
    op.drop_index(op.f('ix_decision_nodes_id'), table_name='decision_nodes')
    op.drop_table('decision_nodes')
    # ### end Alembic commands ###
