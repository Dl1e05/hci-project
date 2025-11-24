"""Add new enum values

Revision ID: a50b25b69e31
Revises: d498b526892c
Create Date: 2025-11-24 05:56:36.370043

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a50b25b69e31'
down_revision: Union[str, Sequence[str], None] = 'd498b526892c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("ALTER TYPE watch_status ADD VALUE IF NOT EXISTS 'read'")
    op.execute("ALTER TYPE watch_status ADD VALUE IF NOT EXISTS 'reading'")
    op.execute("ALTER TYPE watch_status ADD VALUE IF NOT EXISTS 'finished'")
    op.execute("ALTER TYPE watch_status ADD VALUE IF NOT EXISTS 'playing'")


def downgrade() -> None:
    """Downgrade schema."""
    pass
