from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.base import Base

if TYPE_CHECKING:
    from app.content.models.base import BaseContent
    from app.users.models import User

class WatchStatus(str, Enum):
    COMPLETED = "completed"
    PLANNED = "planned"
    DROPPED = "dropped"
    WATCHING = "watching"

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
    status: Mapped[WatchStatus] = mapped_column(watch_status_enum, nullable=False)

    __table_args__ = (UniqueConstraint('user_id', 'content_id', name='uq_user_content'),)

    user: Mapped['User'] = relationship('User', back_populates='content_lists')
    content: Mapped['BaseContent'] = relationship('BaseContent', back_populates='user_lists')
