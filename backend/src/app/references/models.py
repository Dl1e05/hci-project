import uuid
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import URLType

from app.base import Base

if TYPE_CHECKING:
    from app.content.models.base import BaseContent


content_tags = Table(
    'content_tags',
    Base.metadata,
    Column('content_id', PG_UUID(as_uuid=True), ForeignKey('contents.id', ondelete='CASCADE'), primary_key=True),
    Column('tag_id', PG_UUID(as_uuid=True), ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True),
)

content_genres = Table(
    'content_genres',
    Base.metadata,
    Column('content_id', PG_UUID(as_uuid=True), ForeignKey('contents.id', ondelete='CASCADE'), primary_key=True),
    Column('genre_id', PG_UUID(as_uuid=True), ForeignKey('genres.id', ondelete='CASCADE'), primary_key=True),
)

content_audio_languages = Table(
    'content_audio_languages',
    Base.metadata,
    Column('content_id', PG_UUID(as_uuid=True), ForeignKey('contents.id', ondelete='CASCADE'), primary_key=True),
    Column('language_id', Integer, ForeignKey('languages.id', ondelete='CASCADE'), primary_key=True),
)

content_subtitle_languages = Table(
    'content_subtitle_languages',
    Base.metadata,
    Column('content_id', PG_UUID(as_uuid=True), ForeignKey('contents.id', ondelete='CASCADE'), primary_key=True),
    Column('language_id', Integer, ForeignKey('languages.id', ondelete='CASCADE'), primary_key=True),
)


class Tags(Base):
    __tablename__ = 'tags'
    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)

    contents: Mapped[list['BaseContent']] = relationship('BaseContent', secondary=content_tags, back_populates='content_tags')


class Genres(Base):
    __tablename__ = 'genres'
    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)

    contents: Mapped[list['BaseContent']] = relationship('BaseContent', secondary=content_genres, back_populates='genres')


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

    # Relationships
    contents: Mapped[list['BaseContent']] = relationship(
        'BaseContent', foreign_keys='BaseContent.original_language_id', back_populates='original_language'
    )
    audio_contents: Mapped[list['BaseContent']] = relationship(
        'BaseContent', secondary=content_audio_languages, back_populates='audio_languages'
    )
    subtitle_contents: Mapped[list['BaseContent']] = relationship(
        'BaseContent', secondary=content_subtitle_languages, back_populates='subtitle_languages'
    )


class Author(Base):
    __tablename__ = 'authors'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(128), nullable=False, unique=True, index=True)
    link: Mapped[str] = mapped_column(URLType(length=2048), nullable=True)

    # Relationships
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
    description: Mapped[str] = mapped_column(String(255), nullable=False)

    contents: Mapped[list['BaseContent']] = relationship('BaseContent', back_populates='age_rating')


class DifficultyLevel(Base):
    __tablename__ = 'difficulty_levels'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(32), nullable=False, unique=True, index=True)
    level: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)


class ContentCategory(Base):
    __tablename__ = 'content_categories'
    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class ContentType(str, Enum):
    SERIES = 'series'
    BOOK = 'book'
    FILM = 'film'
    ANIME = 'anime'
    PODCAST = 'podcast'
    COURSE = 'course'
    ARTICLE = 'article'
    GAME = 'game'
    VIDEO = 'video'


class UserRating(Base):
    __tablename__ = 'user_ratings'
    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    content_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False, index=True)
    content_type: Mapped[ContentType] = mapped_column(SQLEnum(ContentType), nullable=False, index=True)
    rating: Mapped[float] = mapped_column(Float, nullable=False, index=True)
    review: Mapped[str] = mapped_column(String(1000), nullable=True)
    is_public: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    content: Mapped['BaseContent'] = relationship(
        'BaseContent',
        foreign_keys=[content_id],
        primaryjoin='UserRating.content_id == foreign(BaseContent.id)',
        back_populates='user_ratings',
        viewonly=True,
    )
