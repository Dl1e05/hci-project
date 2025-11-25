from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.base import Base

if TYPE_CHECKING:
    from app.content.models.base import BaseContent
    from app.references.models import DifficultyLevel
    from app.users.models import User


class Review(Base):
    __tablename__ = 'reviews'

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    content_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey('contents.id', ondelete='CASCADE'), nullable=False, index=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True
    )
    commentary: Mapped[str] = mapped_column(Text, nullable=False)
    users_difficulty_level: Mapped[int] = mapped_column(
        Integer, ForeignKey('difficulty_levels.id', ondelete='RESTRICT'), nullable=False, index=True
    )

    # Relationships
    content: Mapped[BaseContent] = relationship(
        'BaseContent',
        foreign_keys=[content_id],
        primaryjoin='Review.content_id == foreign(BaseContent.id)',
        viewonly=True,
    )
    user: Mapped[User] = relationship('User', foreign_keys=[user_id], viewonly=True)
    difficulty_level: Mapped[DifficultyLevel] = relationship(
        'DifficultyLevel', foreign_keys=[users_difficulty_level], viewonly=True
    )
