from __future__ import annotations

from datetime import datetime
from typing import Annotated
from uuid import UUID
from pydantic import Field, StringConstraints, HttpUrl
from app.base import ORMModel

TITLE = Annotated[str, StringConstraints(min_length=1, max_length=128)]
RELEASE_DATE = Annotated[datetime]
RATING = Annotated[float, Field(ge=0.0, le=10.0)]
VIEW_COUNT = Annotated[int, Field(ge=0)]
IS_ACTIVE = Annotated[bool, Field(default=True)]
SHORT_DESCRIPTION = Annotated[str | None, StringConstraints(min_length=1, max_length=500)]
LONG_DESCRIPTION = Annotated[str | None, StringConstraints(min_length=1, max_length=10000)]
TAGS_STRING = Annotated[str | None, StringConstraints(max_length=500)]
KEYWORDS = Annotated[str | None, StringConstraints(max_length=500)]
URL_FIELD = Annotated[HttpUrl | None, Field(max_length=2048)]


class BaseSchema(ORMModel):
    id: UUID
    title: TITLE
    release_date: RELEASE_DATE
    rating: RATING
    view_count: VIEW_COUNT
    is_active: IS_ACTIVE
    short_description: SHORT_DESCRIPTION
    long_description: LONG_DESCRIPTION
    tags: