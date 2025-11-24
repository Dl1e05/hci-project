"""Add content_type and new statuses

Revision ID: d498b526892c
Revises: 44aeff504f92
Create Date: 2025-11-24 05:54:22.881234

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd498b526892c'
down_revision: Union[str, Sequence[str], None] = '44aeff504f92'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Создать enum для content_type
    op.execute("CREATE TYPE content_type AS ENUM ('media', 'games', 'literature')")
    
    # Добавить новые значения в watch_status
    op.execute("ALTER TYPE watch_status ADD VALUE IF NOT EXISTS 'read'")
    op.execute("ALTER TYPE watch_status ADD VALUE IF NOT EXISTS 'reading'")
    op.execute("ALTER TYPE watch_status ADD VALUE IF NOT EXISTS 'finished'")
    op.execute("ALTER TYPE watch_status ADD VALUE IF NOT EXISTS 'playing'")
    
    # Добавить колонку content_type со значением по умолчанию 'media'
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
    # Удалить check constraints
    op.drop_constraint('ck_media_statuses', 'user_content_lists')
    op.drop_constraint('ck_games_statuses', 'user_content_lists')
    op.drop_constraint('ck_literature_statuses', 'user_content_lists')
    
    # Удалить колонку
    op.drop_column('user_content_lists', 'content_type')
    
    # Удалить enum (только если нет других таблиц, использующих его)
    op.execute("DROP TYPE IF EXISTS content_type")