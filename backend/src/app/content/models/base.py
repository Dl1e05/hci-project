from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, func, select
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import URLType

from app.base import Base
from app.references.models import (
    content_audio_languages,
    content_genres,
    content_subtitle_languages,
    content_tags,
)

if TYPE_CHECKING:
    from app.lists.models import UserContentList
    from app.references.models import AgeRating, Author, Country, DifficultyLevel, Genres, Language, Tags, UserRating


class BaseContent(Base):
    __tablename__ = 'contents'

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    content_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    title: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    release_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    _rating: Mapped[float] = mapped_column('rating', Float, nullable=False, default=0.0, index=True)

    view_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    short_description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    long_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    keywords: Mapped[str | None] = mapped_column(String(500), nullable=True)

    banner: Mapped[str | None] = mapped_column(URLType(length=2048), nullable=True)
    trailer: Mapped[str | None] = mapped_column(URLType(length=2048), nullable=True)
    link: Mapped[str | None] = mapped_column(URLType(length=2048), nullable=True)

    original_language_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('languages.id', ondelete='RESTRICT'), nullable=False, index=True
    )
    difficulty_level_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('difficulty_levels.id', ondelete='RESTRICT'), nullable=False, index=True
    )
    age_rating_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('age_ratings.id', ondelete='RESTRICT'), nullable=False, index=True
    )
    original_author_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('authors.id', ondelete='RESTRICT'), nullable=False, index=True
    )
    country_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey('countries.id', ondelete='RESTRICT'), nullable=False, index=True
    )
    difficulty_level_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('difficulty_levels.id', ondelete='RESTRICT'), nullable=False, index=True
    )

    original_language: Mapped[Language] = relationship(
        'Language', foreign_keys=[original_language_id], back_populates='contents'
    )
    difficulty_level: Mapped[DifficultyLevel] = relationship('DifficultyLevel')
    age_rating: Mapped[AgeRating] = relationship('AgeRating', back_populates='contents')
    original_author: Mapped[Author] = relationship('Author', back_populates='contents')
    country: Mapped[Country] = relationship('Country', back_populates='contents')
    difficulty_level: Mapped[DifficultyLevel] = relationship('DifficultyLevel', back_populates='contents')

    content_genres: Mapped[list[Genres]] = relationship('Genres', secondary=content_genres, back_populates='contents')
    audio_languages: Mapped[list[Language]] = relationship(
        'Language', secondary=content_audio_languages, back_populates='audio_contents'
    )
    subtitle_languages: Mapped[list[Language]] = relationship(
        'Language', secondary=content_subtitle_languages, back_populates='subtitle_contents'
    )
    content_tags: Mapped[list[Tags]] = relationship('Tags', secondary=content_tags, back_populates='contents')

    user_ratings: Mapped[list[UserRating]] = relationship(
        'UserRating',
        foreign_keys='UserRating.content_id',
        primaryjoin='BaseContent.id == foreign(UserRating.content_id)',
        viewonly=True,
    )

    user_lists: Mapped[list[UserContentList]] = relationship(
        'UserContentList',
        back_populates='content',
        cascade='all, delete-orphan',
        passive_deletes=True,
    )

    @property
    def rating(self) -> float:
        return self._rating if self._rating is not None else 0.0

    def recalculate_rating(self) -> float:
        from app.references.models import UserRating

        avg_rating = select(func.coalesce(func.avg(UserRating.rating), 0.0)).where(UserRating.content_id == self.id)

        from sqlalchemy.orm import object_session

        session = object_session(self)
        if session:
            result = session.execute(avg_rating).scalar()
            self._rating = float(result) if result is not None else 0.0

        return self._rating

    __mapper_args__ = {
        'polymorphic_on': content_type,
        'polymorphic_identity': 'content',
        'with_polymorphic': '*',
    }
