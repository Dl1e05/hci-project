from __future__ import annotations

import uuid

from sqlalchemy import Boolean, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.content.models.base import BaseContent


class Series(BaseContent):
    __tablename__ = 'series'

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey('contents.id', ondelete='CASCADE'), primary_key=True, index=True
    )
    total_episodes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    current_episode: Mapped[int | None] = mapped_column(Integer, nullable=True, default=1)
    season: Mapped[int | None] = mapped_column(Integer, nullable=True, default=1)
    is_ongoing: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    __mapper_args__ = {'polymorphic_identity': 'series'}


class Book(BaseContent):
    __tablename__ = 'books'

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey('contents.id', ondelete='CASCADE'), primary_key=True, index=True
    )
    pages: Mapped[int | None] = mapped_column(Integer, nullable=True)
    isbn: Mapped[str | None] = mapped_column(String(20), nullable=True, unique=True, index=True)
    edition: Mapped[str | None] = mapped_column(String(50), nullable=True)
    publisher: Mapped[str | None] = mapped_column(String(100), nullable=True)

    __mapper_args__ = {'polymorphic_identity': 'book'}


class Film(BaseContent):
    __tablename__ = 'films'

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey('contents.id', ondelete='CASCADE'), primary_key=True, index=True
    )
    duration_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    director: Mapped[str | None] = mapped_column(String(100), nullable=True)

    __mapper_args__ = {'polymorphic_identity': 'film'}


class Anime(BaseContent):
    __tablename__ = 'animes'

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey('contents.id', ondelete='CASCADE'), primary_key=True, index=True
    )
    total_episodes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    seasons: Mapped[int | None] = mapped_column(Integer, nullable=True, default=1)
    is_ongoing: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    studio: Mapped[str | None] = mapped_column(String(100), nullable=True)

    __mapper_args__ = {'polymorphic_identity': 'anime'}


class Podcast(BaseContent):
    __tablename__ = 'podcasts'

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey('contents.id', ondelete='CASCADE'), primary_key=True, index=True
    )
    total_episodes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    average_duration_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    host: Mapped[str | None] = mapped_column(String(100), nullable=True)
    is_ongoing: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    __mapper_args__ = {'polymorphic_identity': 'podcast'}


class Course(BaseContent):
    __tablename__ = 'courses'

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey('contents.id', ondelete='CASCADE'), primary_key=True, index=True
    )
    total_lessons: Mapped[int | None] = mapped_column(Integer, nullable=True)
    total_duration_hours: Mapped[float | None] = mapped_column(Float, nullable=True)
    difficulty_level: Mapped[str | None] = mapped_column(String(20), nullable=True)
    instructor: Mapped[str | None] = mapped_column(String(100), nullable=True)

    __mapper_args__ = {'polymorphic_identity': 'course'}


class Article(BaseContent):
    __tablename__ = 'articles'

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey('contents.id', ondelete='CASCADE'), primary_key=True, index=True
    )
    word_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    reading_time_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_published: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    __mapper_args__ = {'polymorphic_identity': 'article'}


class Game(BaseContent):
    __tablename__ = 'games'

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey('contents.id', ondelete='CASCADE'), primary_key=True, index=True
    )
    developer: Mapped[str | None] = mapped_column(String(100), nullable=True)
    publisher: Mapped[str | None] = mapped_column(String(100), nullable=True)
    genre: Mapped[str | None] = mapped_column(String(50), nullable=True)
    is_multiplayer: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    __mapper_args__ = {'polymorphic_identity': 'game'}


class Video(BaseContent):
    __tablename__ = 'videos'

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey('contents.id', ondelete='CASCADE'), primary_key=True, index=True
    )
    duration_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    creator: Mapped[str | None] = mapped_column(String(100), nullable=True)

    __mapper_args__ = {'polymorphic_identity': 'video'}
