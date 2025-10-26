from __future__ import annotations

from datetime import datetime
from typing import Annotated
from uuid import UUID
from pydantic import Field, StringConstraints, HttpUrl
from app.base import ORMModel
from app.references.schemas import TagsRead

# Type aliases for content fields
TITLE = Annotated[str, StringConstraints(min_length=1, max_length=128)]
SHORT_DESCRIPTION = Annotated[str | None, StringConstraints(min_length=1, max_length=500)]
LONG_DESCRIPTION = Annotated[str | None, StringConstraints(min_length=1, max_length=10000)]
TAGS_STRING = Annotated[str | None, StringConstraints(max_length=500)]
KEYWORDS = Annotated[str | None, StringConstraints(max_length=500)]
URL_FIELD = Annotated[HttpUrl | None, Field(max_length=2048)]


class BaseContentBase(ORMModel):
    """Base schema for all content types"""
    title: TITLE
    release_date: datetime
    rating: float = Field(..., ge=0.0, le=10.0)
    view_count: int = Field(default=0, ge=0)
    is_active: bool = Field(default=True)
    short_description: SHORT_DESCRIPTION = None
    long_description: LONG_DESCRIPTION = None
    tags: TAGS_STRING = None
    keywords: KEYWORDS = None
    banner: HttpUrl = Field(..., max_length=2048)
    trailer: URL_FIELD = None
    link: URL_FIELD = None
    poster: URL_FIELD = None


class BaseContentCreate(BaseContentBase):
    """Schema for creating content"""
    original_language_id: int
    age_rating_id: int
    original_author_id: int
    country_id: UUID
    genre_ids: list[UUID] = Field(default_factory=list)
    audio_language_ids: list[int] = Field(default_factory=list)
    subtitle_language_ids: list[int] = Field(default_factory=list)
    tag_ids: list[UUID] = Field(default_factory=list)


class BaseContentUpdate(ORMModel):
    """Schema for updating content"""
    title: TITLE | None = None
    release_date: datetime | None = None
    rating: float | None = Field(None, ge=0.0, le=10.0)
    view_count: int | None = Field(None, ge=0)
    is_active: bool | None = None
    short_description: SHORT_DESCRIPTION = None
    long_description: LONG_DESCRIPTION = None
    tags: TAGS_STRING = None
    keywords: KEYWORDS = None
    banner: HttpUrl | None = Field(None, max_length=2048)
    trailer: URL_FIELD = None
    link: URL_FIELD = None
    poster: URL_FIELD = None
    original_language_id: int | None = None
    age_rating_id: int | None = None
    original_author_id: int | None = None
    country_id: UUID | None = None
    genre_ids: list[UUID] | None = None
    audio_language_ids: list[int] | None = None
    subtitle_language_ids: list[int] | None = None
    tag_ids: list[UUID] | None = None


class BaseContentRead(BaseContentBase):
    """Schema for reading content"""
    id: UUID
    original_language_id: int
    age_rating_id: int
    original_author_id: int
    country_id: UUID
    content_tags: list[TagsRead] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime


# Series schemas
class SeriesBase(BaseContentBase):
    """Base schema for series"""
    total_episodes: int | None = Field(None, ge=1)
    current_episode: int | None = Field(None, ge=1)
    season: int | None = Field(None, ge=1)
    is_ongoing: bool = Field(default=True)


class SeriesCreate(SeriesBase, BaseContentCreate):
    """Schema for creating series"""
    pass


class SeriesUpdate(BaseContentUpdate):
    """Schema for updating series"""
    total_episodes: int | None = Field(None, ge=1)
    current_episode: int | None = Field(None, ge=1)
    season: int | None = Field(None, ge=1)
    is_ongoing: bool | None = None


class SeriesRead(SeriesBase, BaseContentRead):
    """Schema for reading series"""
    pass


# Book schemas
class BookBase(BaseContentBase):
    """Base schema for books"""
    pages: int | None = Field(None, ge=1)
    isbn: str | None = Field(None, max_length=20)
    edition: str | None = Field(None, max_length=50)
    publisher: str | None = Field(None, max_length=100)


class BookCreate(BookBase, BaseContentCreate):
    """Schema for creating books"""
    pass


class BookUpdate(BaseContentUpdate):
    """Schema for updating books"""
    pages: int | None = Field(None, ge=1)
    isbn: str | None = Field(None, max_length=20)
    edition: str | None = Field(None, max_length=50)
    publisher: str | None = Field(None, max_length=100)


class BookRead(BookBase, BaseContentRead):
    """Schema for reading books"""
    pass


# Film schemas
class FilmBase(BaseContentBase):
    """Base schema for films"""
    duration_minutes: int | None = Field(None, ge=1)
    director: str | None = Field(None, max_length=100)


class FilmCreate(FilmBase, BaseContentCreate):
    """Schema for creating films"""
    pass


class FilmUpdate(BaseContentUpdate):
    """Schema for updating films"""
    duration_minutes: int | None = Field(None, ge=1)
    director: str | None = Field(None, max_length=100)


class FilmRead(FilmBase, BaseContentRead):
    """Schema for reading films"""
    pass


# Anime schemas
class AnimeBase(BaseContentBase):
    """Base schema for anime"""
    total_episodes: int | None = Field(None, ge=1)
    seasons: int | None = Field(None, ge=1)
    is_ongoing: bool = Field(default=True)
    studio: str | None = Field(None, max_length=100)


class AnimeCreate(AnimeBase, BaseContentCreate):
    """Schema for creating anime"""
    pass


class AnimeUpdate(BaseContentUpdate):
    """Schema for updating anime"""
    total_episodes: int | None = Field(None, ge=1)
    seasons: int | None = Field(None, ge=1)
    is_ongoing: bool | None = None
    studio: str | None = Field(None, max_length=100)


class AnimeRead(AnimeBase, BaseContentRead):
    """Schema for reading anime"""
    pass


# Podcast schemas
class PodcastBase(BaseContentBase):
    """Base schema for podcasts"""
    total_episodes: int | None = Field(None, ge=1)
    average_duration_minutes: int | None = Field(None, ge=1)
    host: str | None = Field(None, max_length=100)
    is_ongoing: bool = Field(default=True)


class PodcastCreate(PodcastBase, BaseContentCreate):
    """Schema for creating podcasts"""
    pass


class PodcastUpdate(BaseContentUpdate):
    """Schema for updating podcasts"""
    total_episodes: int | None = Field(None, ge=1)
    average_duration_minutes: int | None = Field(None, ge=1)
    host: str | None = Field(None, max_length=100)
    is_ongoing: bool | None = None


class PodcastRead(PodcastBase, BaseContentRead):
    """Schema for reading podcasts"""
    pass


# Course schemas
class CourseBase(BaseContentBase):
    """Base schema for courses"""
    total_lessons: int | None = Field(None, ge=1)
    total_duration_hours: float | None = Field(None, ge=0.0)
    difficulty_level: str | None = Field(None, max_length=20)
    instructor: str | None = Field(None, max_length=100)


class CourseCreate(CourseBase, BaseContentCreate):
    """Schema for creating courses"""
    pass


class CourseUpdate(BaseContentUpdate):
    """Schema for updating courses"""
    total_lessons: int | None = Field(None, ge=1)
    total_duration_hours: float | None = Field(None, ge=0.0)
    difficulty_level: str | None = Field(None, max_length=20)
    instructor: str | None = Field(None, max_length=100)


class CourseRead(CourseBase, BaseContentRead):
    """Schema for reading courses"""
    pass


# Article schemas
class ArticleBase(BaseContentBase):
    """Base schema for articles"""
    word_count: int | None = Field(None, ge=1)
    reading_time_minutes: int | None = Field(None, ge=1)
    is_published: bool = Field(default=True)


class ArticleCreate(ArticleBase, BaseContentCreate):
    """Schema for creating articles"""
    pass


class ArticleUpdate(BaseContentUpdate):
    """Schema for updating articles"""
    word_count: int | None = Field(None, ge=1)
    reading_time_minutes: int | None = Field(None, ge=1)
    is_published: bool | None = None


class ArticleRead(ArticleBase, BaseContentRead):
    """Schema for reading articles"""
    pass


# Game schemas
class GameBase(BaseContentBase):
    """Base schema for games"""
    developer: str | None = Field(None, max_length=100)
    publisher: str | None = Field(None, max_length=100)
    genre: str | None = Field(None, max_length=50)
    is_multiplayer: bool = Field(default=False)


class GameCreate(GameBase, BaseContentCreate):
    """Schema for creating games"""
    pass


class GameUpdate(BaseContentUpdate):
    """Schema for updating games"""
    developer: str | None = Field(None, max_length=100)
    publisher: str | None = Field(None, max_length=100)
    genre: str | None = Field(None, max_length=50)
    is_multiplayer: bool | None = None


class GameRead(GameBase, BaseContentRead):
    """Schema for reading games"""
    pass


# Video schemas
class VideoBase(BaseContentBase):
    """Base schema for videos"""
    duration_minutes: int | None = Field(None, ge=1)
    creator: str | None = Field(None, max_length=100)


class VideoCreate(VideoBase, BaseContentCreate):
    """Schema for creating videos"""
    pass


class VideoUpdate(BaseContentUpdate):
    """Schema for updating videos"""
    duration_minutes: int | None = Field(None, ge=1)
    creator: str | None = Field(None, max_length=100)


class VideoRead(VideoBase, BaseContentRead):
    """Schema for reading videos"""
    pass
