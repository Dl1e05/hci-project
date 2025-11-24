from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class ContentFilterParams(BaseModel):
    """Filter parameters for content queries"""

    # Search
    search: str | None = Field(None, description='Search in title, short_description, long_description, and keywords')

    # Filtering by relationships
    genre_ids: list[int] | None = Field(None, description='Filter by genre IDs')
    tag_ids: list[int] | None = Field(None, description='Filter by tag IDs')
    audio_language_ids: list[int] | None = Field(None, description='Filter by audio language IDs')
    subtitle_language_ids: list[int] | None = Field(None, description='Filter by subtitle language IDs')
    original_language_id: int | None = Field(None, description='Filter by original language ID')
    age_rating_id: int | None = Field(None, description='Filter by age rating ID')
    author_id: int | None = Field(None, description='Filter by author ID')
    country_id: UUID | None = Field(None, description='Filter by country ID')

    # Filtering by scalar fields
    min_rating: float | None = Field(None, ge=0, le=10, description='Minimum rating')
    max_rating: float | None = Field(None, ge=0, le=10, description='Maximum rating')
    release_date_from: datetime | None = Field(None, description='Filter content released after this date')
    release_date_to: datetime | None = Field(None, description='Filter content released before this date')
    is_active: bool | None = Field(None, description='Filter by active status')

    # Sorting
    sort_by: Literal['title', 'release_date', 'rating', 'view_count', 'created_at'] | None = Field(
        None, description='Field to sort by'
    )
    sort_order: Literal['asc', 'desc'] = Field('desc', description='Sort order (asc or desc)')


class BookFilterParams(ContentFilterParams):
    """Filter parameters specific to books"""

    isbn: str | None = Field(None, description='Filter by ISBN')
    publisher: str | None = Field(None, description='Filter by publisher (partial match)')
    min_pages: int | None = Field(None, ge=1, description='Minimum number of pages')
    max_pages: int | None = Field(None, ge=1, description='Maximum number of pages')


class SeriesFilterParams(ContentFilterParams):
    """Filter parameters specific to series"""

    is_ongoing: bool | None = Field(None, description='Filter by ongoing status')
    min_episodes: int | None = Field(None, ge=1, description='Minimum number of episodes')
    max_episodes: int | None = Field(None, ge=1, description='Maximum number of episodes')
    season: int | None = Field(None, ge=1, description='Filter by season number')


class AnimeFilterParams(ContentFilterParams):
    """Filter parameters specific to anime"""

    is_ongoing: bool | None = Field(None, description='Filter by ongoing status')
    studio: str | None = Field(None, description='Filter by studio (partial match)')
    min_episodes: int | None = Field(None, ge=1, description='Minimum number of episodes')
    max_episodes: int | None = Field(None, ge=1, description='Maximum number of episodes')


class FilmFilterParams(ContentFilterParams):
    """Filter parameters specific to films"""

    director: str | None = Field(None, description='Filter by director (partial match)')
    min_duration: int | None = Field(None, ge=1, description='Minimum duration in minutes')
    max_duration: int | None = Field(None, ge=1, description='Maximum duration in minutes')


class PodcastFilterParams(ContentFilterParams):
    """Filter parameters specific to podcasts"""

    is_ongoing: bool | None = Field(None, description='Filter by ongoing status')
    host: str | None = Field(None, description='Filter by host (partial match)')
    min_episodes: int | None = Field(None, ge=1, description='Minimum number of episodes')
    max_episodes: int | None = Field(None, ge=1, description='Maximum number of episodes')


class CourseFilterParams(ContentFilterParams):
    """Filter parameters specific to courses"""

    difficulty_level: str | None = Field(None, description='Filter by difficulty level')
    instructor: str | None = Field(None, description='Filter by instructor (partial match)')
    min_lessons: int | None = Field(None, ge=1, description='Minimum number of lessons')
    max_lessons: int | None = Field(None, ge=1, description='Maximum number of lessons')
    min_duration_hours: float | None = Field(None, ge=0, description='Minimum duration in hours')
    max_duration_hours: float | None = Field(None, ge=0, description='Maximum duration in hours')


class ArticleFilterParams(ContentFilterParams):
    """Filter parameters specific to articles"""

    is_published: bool | None = Field(None, description='Filter by published status')
    min_word_count: int | None = Field(None, ge=1, description='Minimum word count')
    max_word_count: int | None = Field(None, ge=1, description='Maximum word count')
    min_reading_time: int | None = Field(None, ge=1, description='Minimum reading time in minutes')
    max_reading_time: int | None = Field(None, ge=1, description='Maximum reading time in minutes')


class GameFilterParams(ContentFilterParams):
    """Filter parameters specific to games"""

    developer: str | None = Field(None, description='Filter by developer (partial match)')
    publisher: str | None = Field(None, description='Filter by publisher (partial match)')
    genre: str | None = Field(None, description='Filter by genre')
    is_multiplayer: bool | None = Field(None, description='Filter by multiplayer support')


class VideoFilterParams(ContentFilterParams):
    """Filter parameters specific to videos"""

    creator: str | None = Field(None, description='Filter by creator (partial match)')
    min_duration: int | None = Field(None, ge=1, description='Minimum duration in minutes')
    max_duration: int | None = Field(None, ge=1, description='Maximum duration in minutes')
