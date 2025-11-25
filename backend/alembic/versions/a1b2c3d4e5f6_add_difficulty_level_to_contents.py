"""add difficulty level to contents

Revision ID: a1b2c3d4e5f6
Revises: fa274471e8e8
Create Date: 2025-11-16 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = 'fa274471e8e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop the old difficulty_level column from courses table (if it exists)
    op.drop_column('courses', 'difficulty_level')

    # Add difficulty_level_id column to contents table
    op.add_column('contents', sa.Column('difficulty_level_id', sa.Integer(), nullable=False, server_default='1'))
    op.create_index(op.f('ix_contents_difficulty_level_id'), 'contents', ['difficulty_level_id'], unique=False)
    op.create_foreign_key(
        op.f('contents_difficulty_level_id_fkey'),
        'contents',
        'difficulty_levels',
        ['difficulty_level_id'],
        ['id'],
        ondelete='RESTRICT'
    )

    # Remove server_default after adding the column
    op.alter_column('contents', 'difficulty_level_id', server_default=None)


def downgrade() -> None:
    """Downgrade schema."""
    # Remove difficulty_level_id from contents table
    op.drop_constraint(op.f('contents_difficulty_level_id_fkey'), 'contents', type_='foreignkey')
    op.drop_index(op.f('ix_contents_difficulty_level_id'), table_name='contents')
    op.drop_column('contents', 'difficulty_level_id')

    # Re-add difficulty_level column to courses table
    op.add_column('courses', sa.Column('difficulty_level', sa.VARCHAR(length=20), autoincrement=False, nullable=True))