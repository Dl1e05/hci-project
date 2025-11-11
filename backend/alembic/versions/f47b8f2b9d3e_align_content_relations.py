"""align content relations

Revision ID: f47b8f2b9d3e
Revises: ee34c87de85b
Create Date: 2025-10-31 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "f47b8f2b9d3e"
down_revision: Union[str, Sequence[str], None] = "ee34c87de85b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


CONTENT_TABLES = [
    "series",
    "books",
    "films",
    "animes",
    "podcasts",
    "courses",
    "articles",
    "games",
    "videos",
]


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("contents", "type", new_column_name="content_type")

    for table_name in CONTENT_TABLES:
        op.alter_column(table_name, "id", new_column_name="content_id")


def downgrade() -> None:
    """Downgrade schema."""
    for table_name in CONTENT_TABLES:
        op.alter_column(table_name, "content_id", new_column_name="id")

    op.rename_index("ix_contents_content_type", "ix_contents_type")
    op.alter_column("contents", "content_type", new_column_name="type")


