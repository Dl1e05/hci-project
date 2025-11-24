"""Add content_type field and constraints

Revision ID: 6c7e591e227e
Revises: d69350c6efa3
Create Date: 2025-11-24 06:00:50.160378

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6c7e591e227e'
down_revision: Union[str, Sequence[str], None] = 'd69350c6efa3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Создать enum для content_type
    op.execute("CREATE TYPE content_type AS ENUM ('media', 'games', 'literature')")
    
    # Добавить колонку
    op.execute("""
        ALTER TABLE user_content_lists 
        ADD COLUMN content_type content_type DEFAULT 'media' NOT NULL
    """)
    
    # Добавить check constraints
    op.create_check_constraint(
        'ck_media_statuses',
        'user_content_lists',
        "(content_type != 'media') OR (status IN ('completed', 'planned', 'dropped', 'watching', 'postponed'))"
    )
    
    op.create_check_constraint(
        'ck_games_statuses',
        'user_content_lists',
        "(content_type != 'games') OR (status IN ('finished', 'playing', 'planned', 'dropped', 'postponed'))"
    )
    
    op.create_check_constraint(
        'ck_literature_statuses',
        'user_content_lists',
        "(content_type != 'literature') OR (status IN ('read', 'reading', 'planned', 'dropped', 'postponed'))"
    )

def downgrade():
    op.drop_constraint('ck_media_statuses', 'user_content_lists')
    op.drop_constraint('ck_games_statuses', 'user_content_lists')
    op.drop_constraint('ck_literature_statuses', 'user_content_lists')
    op.drop_column('user_content_lists', 'content_type')
    op.execute("DROP TYPE IF EXISTS content_type")
