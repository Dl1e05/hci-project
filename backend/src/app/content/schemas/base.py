from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import Field, HttpUrl, StringConstraints

from app.base import ORMModel
from app.references.schemas import TagsRead

TITLE = Annotated[str, StringConstraints(min_length=1, max_length=128)]
SHORT_DESCRIPTION = Annotated[str | None, StringConstraints(min_length=1, max_length=500)]
LONG_DESCRIPTION = Annotated[str | None, StringConstraints(min_length=1, max_length=10000)]
KEYWORDS = Annotated[str | None, StringConstraints(max_length=500)]
URL_FIELD = Annotated[HttpUrl | None, Field(max_length=2048)]


class BaseContentBase(ORMModel):
    title: TITLE
    release_date: datetime
    is_active: bool = Field(default=True)
    short_description: SHORT_DESCRIPTION = None
    long_description: LONG_DESCRIPTION = None
    keywords: KEYWORDS = None
    banner: HttpUrl | None = Field(None, max_length=2048)
    trailer: URL_FIELD = None
    link: URL_FIELD = None


class BaseContentCreate(BaseContentBase):
    original_language_id: int
    difficulty_level_id: int
    age_rating_id: int
    original_author_id: int
    country_id: UUID
    genre_ids: list[UUID] = Field(default_factory=list)
    audio_language_ids: list[int] = Field(default_factory=list)
    subtitle_language_ids: list[int] = Field(default_factory=list)
    tag_ids: list[UUID] = Field(default_factory=list)


class BaseContentUpdate(ORMModel):
    title: TITLE | None = None
    release_date: datetime | None = None
    is_active: bool | None = None
    short_description: SHORT_DESCRIPTION = None
    long_description: LONG_DESCRIPTION = None
    keywords: KEYWORDS = None
    banner: HttpUrl | None = Field(None, max_length=2048)
    trailer: URL_FIELD = None
    link: URL_FIELD = None
    original_language_id: int | None = None
    difficulty_level_id: int | None = None
    age_rating_id: int | None = None
    original_author_id: int | None = None
    country_id: UUID | None = None
    genre_ids: list[UUID] | None = None
    audio_language_ids: list[int] | None = None
    subtitle_language_ids: list[int] | None = None
    tag_ids: list[UUID] | None = None


class BaseContentRead(BaseContentBase):
    id: UUID
    view_count: int = Field(ge=0)
    rating: float = Field(..., ge=0.0, le=10.0)
    original_language_id: int
    difficulty_level_id: int
    age_rating_id: int
    original_author_id: int
    country_id: UUID
    content_tags: list[TagsRead] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
