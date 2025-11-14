"""Fix watch list relations

Revision ID: 4c47a5350723
Revises: c451801ef4ed
Create Date: 2025-11-13 15:22:48.186189

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '4c47a5350723'
down_revision: Union[str, Sequence[str], None] = 'c451801ef4ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    watch_status_enum = postgresql.ENUM(
        'completed',
        'planned',
        'dropped',
        name='watch_status',
        create_type=False,
    )

    # Create new enum type if it does not exist
    watch_status_enum.create(op.get_bind(), checkfirst=True)

    # Normalize existing values to lowercase before casting
    op.execute("UPDATE user_content_lists SET status = lower(status::text)::watchstatus")

    # Alter the column to use the new enum and keep data
    op.alter_column(
        'user_content_lists',
        'status',
        existing_type=postgresql.ENUM('COMPLETED', 'PLANNED', 'DROPPED', name='watchstatus'),
        type_=watch_status_enum,
        postgresql_using="status::text::watch_status",
        existing_nullable=False,
    )

    # Drop the old enum type
    op.execute('DROP TYPE IF EXISTS watchstatus')

    op.drop_constraint(op.f('user_content_lists_user_id_fkey'), 'user_content_lists', type_='foreignkey')
    op.create_foreign_key(None, 'user_content_lists', 'users', ['user_id'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    """Downgrade schema."""
    watch_status_enum = postgresql.ENUM(
        'completed',
        'planned',
        'dropped',
        name='watch_status',
        create_type=False,
    )
    old_watchstatus_enum = postgresql.ENUM(
        'COMPLETED',
        'PLANNED',
        'DROPPED',
        name='watchstatus',
        create_type=False,
    )

    # Re-create the old enum if needed
    old_watchstatus_enum.create(op.get_bind(), checkfirst=True)

    op.drop_constraint(None, 'user_content_lists', type_='foreignkey')
    op.create_foreign_key(
        op.f('user_content_lists_user_id_fkey'),
        'user_content_lists',
        'users',
        ['user_id'],
        ['id'],
    )

    # Convert values back to uppercase before casting
    op.execute("UPDATE user_content_lists SET status = upper(status::text)::watch_status")

    op.alter_column(
        'user_content_lists',
        'status',
        existing_type=watch_status_enum,
        type_=old_watchstatus_enum,
        postgresql_using="status::text::watchstatus",
        existing_nullable=False,
    )

    watch_status_enum.drop(op.get_bind(), checkfirst=True)
