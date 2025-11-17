"""Fix watch_status enum values

Revision ID: 5564e757a505
Revises: c6db5f9e7703
Create Date: 2025-11-17 11:44:37.529950

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5564e757a505'
down_revision: Union[str, Sequence[str], None] = 'c6db5f9e7703'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
