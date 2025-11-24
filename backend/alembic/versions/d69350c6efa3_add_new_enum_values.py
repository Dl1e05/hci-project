"""Add new enum values

Revision ID: d69350c6efa3
Revises: a50b25b69e31
Create Date: 2025-11-24 05:58:28.568901

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd69350c6efa3'
down_revision: Union[str, Sequence[str], None] = 'a50b25b69e31'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Добавляем новые значения - каждая команда автоматически коммитится
    op.execute("ALTER TYPE watch_status ADD VALUE IF NOT EXISTS 'read'")
    op.execute("ALTER TYPE watch_status ADD VALUE IF NOT EXISTS 'reading'")
    op.execute("ALTER TYPE watch_status ADD VALUE IF NOT EXISTS 'finished'")
    op.execute("ALTER TYPE watch_status ADD VALUE IF NOT EXISTS 'playing'")


def downgrade() -> None:
    """Downgrade schema."""
    pass
