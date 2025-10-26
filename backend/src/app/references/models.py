import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Table, Float, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import URLType

from app.base import Base

if TYPE_CHECKING:
    from app.content.models.base import BaseContent

content_type_tags = Table(
    'content_type_tags',
    Base.metadata,
    Column('content_type_id', PG_UUID(as_uuid=True), ForeignKey('content_types.id', ondelete='CASCADE'), primary_key=True),
    Column('tag_id', PG_UUID(as_uuid=True), ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True),
)


class Tags(Base):
    __tablename__ = 'tags'

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    code: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)

    content_types: Mapped[list['ContentType']] = relationship('ContentType', secondary=content_type_tags, back_populates='tags')
    contents: Mapped[list['BaseContent']] = relationship('BaseContent', secondary='content_tags', back_populates='content_tags')


class ContentType(Base):
    __tablename__ = 'content_types'

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    order: Mapped[int] = mapped_column(Integer, nullable=False, index=True)

    tags: Mapped[list['Tags']] = relationship('Tags', secondary=content_type_tags, back_populates='content_types')


class Genres(Base):
    __tablename__ = 'genres'

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)

    contents: Mapped[list['BaseContent']] = relationship('BaseContent', secondary='content_genres', back_populates='genres')


class Country(Base):
    __tablename__ = 'countries'

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)
    code: Mapped[str] = mapped_column(String(2), nullable=False, unique=True, index=True)

    contents: Mapped[list['BaseContent']] = relationship('BaseContent', back_populates='country')



class Language(Base):
    __tablename__ = 'languages'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)
    code: Mapped[str] = mapped_column(String(2), nullable=False, unique=True, index=True)

    contents: Mapped[list['BaseContent']] = relationship('BaseContent', foreign_keys='BaseContent.original_language_id', back_populates='original_language')
    audio_contents: Mapped[list['BaseContent']] = relationship('BaseContent', secondary='content_audio_languages', back_populates='audio_languages')
    subtitle_contents: Mapped[list['BaseContent']] = relationship('BaseContent', secondary='content_subtitle_languages', back_populates='subtitle_languages')


class Author(Base):
    __tablename__ = 'authors'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(128), nullable=False, unique=True, index=True)
    link: Mapped[str] = mapped_column(URLType(length=2048), nullable=True)

    contents: Mapped[list['BaseContent']] = relationship('BaseContent', back_populates='original_author')


class Platform(Base):
    __tablename__ = 'platforms'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)


class AgeRating(Base):
    __tablename__ = 'age_ratings'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(32), nullable=False, unique=True, index=True)
    value: Mapped[str] = mapped_column(String(32), nullable=False, unique=True, index=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)

    contents: Mapped[list['BaseContent']] = relationship('BaseContent', back_populates='age_rating')


class DifficultyLevel(Base):
    __tablename__ = 'difficulty_levels'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(32), nullable=False, unique=True, index=True)
    level: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    min_score: Mapped[float] = mapped_column(Float, nullable=False)
    max_score: Mapped[float] = mapped_column(Float, nullable=False)


class ContentStatus(Base):
    __tablename__ = 'content_statuses'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(32), nullable=False, unique=True, index=True)
    description: Mapped[str] = mapped_column(String(255), nullable=True)


class ContentCategory(Base):
    __tablename__ = 'content_categories'

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    parent_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey('content_categories.id'), nullable=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    parent: Mapped['ContentCategory'] = relationship('ContentCategory', remote_side=[id], back_populates='children')
    children: Mapped[list['ContentCategory']] = relationship('ContentCategory', back_populates='parent')


class UserRating(Base):
    __tablename__ = 'user_ratings'

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    content_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False, index=True)  # Generic content reference
    content_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    rating: Mapped[float] = mapped_column(Float, nullable=False, index=True)
    review: Mapped[str] = mapped_column(String(1000), nullable=True)
    is_public: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


class UserProgress(Base):
    __tablename__ = 'user_progress'

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    content_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False, index=True)  # Generic content reference
    content_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    progress_percentage: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    current_position: Mapped[int] = mapped_column(Integer, nullable=True)  # For episodes, pages, etc.
    is_completed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    last_accessed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)


