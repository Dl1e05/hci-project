"""add_content_tags_table

Revision ID: 5c608340af5d
Revises: 8fdf2d1d3642
Create Date: 2025-10-26 15:37:18.781753

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '5c608340af5d'
down_revision: Union[str, Sequence[str], None] = '8fdf2d1d3642'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create content_tags table
    op.create_table('content_tags',
        sa.Column('content_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('tag_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(['content_id'], ['contents.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('content_id', 'tag_id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop content_tags table
    op.drop_table('content_tags')
