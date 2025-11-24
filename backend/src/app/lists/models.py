from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, Enum as SQLEnum
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.base import Base

if TYPE_CHECKING:
    from app.content.models.base import BaseContent
    from app.users.models import User

class ContentType(str, Enum):
    MEDIA = "media"
    GAMES = "games"
    LITERATURE = "literature"

class WatchStatus(str, Enum):
    COMPLETED = "completed"
    PLANNED = "planned"
    DROPPED = "dropped"
    WATCHING = "watching"
    POSTPONED = "postponed"

    READ = "read"
    READING = "reading"

    FINISHED = "finished"
    PLAYING = "playing"

content_type_enum = SQLEnum(
    ContentType,
    name='content_type',
    values_callable=lambda enum: [member.value for member in enum],
)

watch_status_enum = SQLEnum(
    WatchStatus,
    name='watch_status',
    values_callable=lambda enum: [member.value for member in enum],
)


class UserContentList(Base):
    __tablename__ = 'user_content_lists'

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
    )
    content_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey('contents.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
    )
    content_type: Mapped[ContentType] = mapped_column(content_type_enum, nullable=False)
    status: Mapped[WatchStatus] = mapped_column(watch_status_enum, nullable=False)

    __table_args__ = (
        UniqueConstraint('user_id', 'content_id', name='uq_user_content'),

        CheckConstraint(
            "(content_type != 'media') OR (status IN ('completed', 'planned', 'dropped', 'watching', 'postponed'))",
            name='ck_media_statuses'
        ),
        
        CheckConstraint(
            "(content_type != 'games') OR (status IN ('finished', 'playing', 'planned', 'dropped', 'postponed'))",
            name='ck_games_statuses'
        ),
        
        CheckConstraint(
            "(content_type != 'literature') OR (status IN ('read', 'reading', 'planned', 'dropped', 'postponed'))",
            name='ck_literature_statuses'
        ),
    )

    user: Mapped['User'] = relationship('User', back_populates='content_lists')
    content: Mapped['BaseContent'] = relationship('BaseContent', back_populates='user_lists')
