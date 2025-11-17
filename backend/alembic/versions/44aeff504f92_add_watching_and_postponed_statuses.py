"""Add watching and postponed statuses

Revision ID: 44aeff504f92
Revises: 5564e757a505
Create Date: 2025-11-17 11:57:35.194633

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '44aeff504f92'
down_revision: Union[str, Sequence[str], None] = '5564e757a505'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TYPE watch_status ADD VALUE IF NOT EXISTS 'watching'")
    op.execute("ALTER TYPE watch_status ADD VALUE IF NOT EXISTS 'postponed'")


def downgrade() -> None:
    """Downgrade schema."""
    pass
