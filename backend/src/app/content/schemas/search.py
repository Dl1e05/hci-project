from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

from app.content.schemas.content import (
    AnimeRead,
    ArticleRead,
    BookRead,
    CourseRead,
    FilmRead,
    GameRead,
    PodcastRead,
    SeriesRead,
    VideoRead,
)


class ContentSearchParams(BaseModel):
    search: str | None = Field(None, min_length=1, max_length=200)

    title: str | None = Field(None, min_length=1, max_length=128)
    short_description: str | None = Field(None, min_length=1, max_length=500)
    long_description: str | None = Field(None, min_length=1, max_length=10000)
    keywords: str | None = Field(None, min_length=1, max_length=500)

    content_types: list[Literal['series', 'book', 'film', 'anime', 'podcast', 'course', 'article', 'game', 'video']] | None = (
        None
    )

    genre_ids: list[UUID] | None = None
    tag_ids: list[UUID] | None = None
    audio_language_ids: list[int] | None = None
    subtitle_language_ids: list[int] | None = None
    original_language_id: int | None = None
    age_rating_id: int | None = None
    author_id: int | None = None
    country_id: UUID | None = None
    difficulty_level_id: int | None = None

    min_rating: float | None = Field(None, ge=0, le=10)
    max_rating: float | None = Field(None, ge=0, le=10)
    release_date_from: datetime | None = None
    release_date_to: datetime | None = None
    is_active: bool | None = None

    sort_by: Literal['title', 'release_date', 'rating', 'view_count', 'created_at'] | None = Field('created_at')
    sort_order: Literal['asc', 'desc'] = Field('desc')

    skip: int = Field(0, ge=0)
    limit: int = Field(20, ge=1, le=100)


class ContentSearchResult(BaseModel):
    items: list[SeriesRead | BookRead | FilmRead | AnimeRead | PodcastRead | CourseRead | ArticleRead | GameRead | VideoRead]
    total: int = Field(..., ge=0)
    skip: int = Field(..., ge=0)
    limit: int = Field(..., ge=1)
