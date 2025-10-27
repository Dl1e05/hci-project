from __future__ import annotations
from pydantic import Field
from .base import BaseContentBase, BaseContentUpdate, BaseContentCreate, BaseContentRead


class SeriesCreate(BaseContentCreate):
    total_episodes: int | None = Field(None, ge=1)
    current_episode: int | None = Field(None, ge=1)
    season: int | None = Field(None, ge=1)
    is_ongoing: bool = Field(default=True)


class SeriesUpdate(BaseContentUpdate):
    total_episodes: int | None = Field(None, ge=1)
    current_episode: int | None = Field(None, ge=1)
    season: int | None = Field(None, ge=1)
    is_ongoing: bool | None = None


class SeriesRead(BaseContentRead):
    total_episodes: int | None = Field(None, ge=1)
    current_episode: int | None = Field(None, ge=1)
    season: int | None = Field(None, ge=1)
    is_ongoing: bool = Field(default=True)


# Book schemas
class BookCreate(BaseContentCreate):
    pages: int | None = Field(None, ge=1)
    isbn: str | None = Field(None, max_length=20)
    edition: str | None = Field(None, max_length=50)
    publisher: str | None = Field(None, max_length=100)


class BookUpdate(BaseContentUpdate):
    pages: int | None = Field(None, ge=1)
    isbn: str | None = Field(None, max_length=20)
    edition: str | None = Field(None, max_length=50)
    publisher: str | None = Field(None, max_length=100)


class BookRead(BaseContentRead):
    pages: int | None = Field(None, ge=1)
    isbn: str | None = Field(None, max_length=20)
    edition: str | None = Field(None, max_length=50)
    publisher: str | None = Field(None, max_length=100)


# Film schemas
class FilmCreate(BaseContentCreate):
    duration_minutes: int | None = Field(None, ge=1)
    director: str | None = Field(None, max_length=100)


class FilmUpdate(BaseContentUpdate):
    duration_minutes: int | None = Field(None, ge=1)
    director: str | None = Field(None, max_length=100)


class FilmRead(BaseContentRead):
    duration_minutes: int | None = Field(None, ge=1)
    director: str | None = Field(None, max_length=100)


class AnimeCreate(BaseContentCreate):
    total_episodes: int | None = Field(None, ge=1)
    seasons: int | None = Field(None, ge=1)
    is_ongoing: bool = Field(default=True)
    studio: str | None = Field(None, max_length=100)


class AnimeUpdate(BaseContentUpdate):
    total_episodes: int | None = Field(None, ge=1)
    seasons: int | None = Field(None, ge=1)
    is_ongoing: bool | None = None
    studio: str | None = Field(None, max_length=100)


class AnimeRead(BaseContentRead):
    total_episodes: int | None = Field(None, ge=1)
    seasons: int | None = Field(None, ge=1)
    is_ongoing: bool = Field(default=True)
    studio: str | None = Field(None, max_length=100)


# Podcast schemas
class PodcastCreate(BaseContentCreate):
    total_episodes: int | None = Field(None, ge=1)
    average_duration_minutes: int | None = Field(None, ge=1)
    host: str | None = Field(None, max_length=100)
    is_ongoing: bool = Field(default=True)


class PodcastUpdate(BaseContentUpdate):
    total_episodes: int | None = Field(None, ge=1)
    average_duration_minutes: int | None = Field(None, ge=1)
    host: str | None = Field(None, max_length=100)
    is_ongoing: bool | None = None


class PodcastRead(BaseContentRead):
    total_episodes: int | None = Field(None, ge=1)
    average_duration_minutes: int | None = Field(None, ge=1)
    host: str | None = Field(None, max_length=100)
    is_ongoing: bool = Field(default=True)


# Course schemas
class CourseCreate(BaseContentCreate):
    total_lessons: int | None = Field(None, ge=1)
    total_duration_hours: float | None = Field(None, ge=0.0)
    difficulty_level: str | None = Field(None, max_length=20)
    instructor: str | None = Field(None, max_length=100)


class CourseUpdate(BaseContentUpdate):
    total_lessons: int | None = Field(None, ge=1)
    total_duration_hours: float | None = Field(None, ge=0.0)
    difficulty_level: str | None = Field(None, max_length=20)
    instructor: str | None = Field(None, max_length=100)


class CourseRead(BaseContentRead):
    total_lessons: int | None = Field(None, ge=1)
    total_duration_hours: float | None = Field(None, ge=0.0)
    difficulty_level: str | None = Field(None, max_length=20)
    instructor: str | None = Field(None, max_length=100)


class ArticleCreate(BaseContentCreate):
    word_count: int | None = Field(None, ge=1)
    reading_time_minutes: int | None = Field(None, ge=1)
    is_published: bool = Field(default=True)


class ArticleUpdate(BaseContentUpdate):
    word_count: int | None = Field(None, ge=1)
    reading_time_minutes: int | None = Field(None, ge=1)
    is_published: bool | None = None


class ArticleRead(BaseContentRead):
    word_count: int | None = Field(None, ge=1)
    reading_time_minutes: int | None = Field(None, ge=1)
    is_published: bool = Field(default=True)


# Game schemas
class GameCreate(BaseContentCreate):
    developer: str | None = Field(None, max_length=100)
    publisher: str | None = Field(None, max_length=100)
    genre: str | None = Field(None, max_length=50)
    is_multiplayer: bool = Field(default=False)


class GameUpdate(BaseContentUpdate):
    developer: str | None = Field(None, max_length=100)
    publisher: str | None = Field(None, max_length=100)
    genre: str | None = Field(None, max_length=50)
    is_multiplayer: bool | None = None


class GameRead(BaseContentRead):
    developer: str | None = Field(None, max_length=100)
    publisher: str | None = Field(None, max_length=100)
    genre: str | None = Field(None, max_length=50)
    is_multiplayer: bool = Field(default=False)


# Video schemas
class VideoCreate(BaseContentCreate):
    duration_minutes: int | None = Field(None, ge=1)
    creator: str | None = Field(None, max_length=100)


class VideoUpdate(BaseContentUpdate):
    duration_minutes: int | None = Field(None, ge=1)
    creator: str | None = Field(None, max_length=100)


class VideoRead(BaseContentRead):
    duration_minutes: int | None = Field(None, ge=1)
    creator: str | None = Field(None, max_length=100)
