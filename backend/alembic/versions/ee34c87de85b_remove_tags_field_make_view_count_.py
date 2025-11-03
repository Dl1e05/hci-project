"""remove_tags_field_make_view_count_readonly

Revision ID: ee34c87de85b
Revises: dc5657b362f0
Create Date: 2025-10-27 19:31:44.775207

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ee34c87de85b'
down_revision: Union[str, Sequence[str], None] = 'dc5657b362f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Remove the tags string field from contents table
    op.drop_column('contents', 'tags')


def downgrade() -> None:
    """Downgrade schema."""
    # Add back the tags string field
    op.add_column('contents', sa.Column('tags', sa.String(length=500), nullable=True))
