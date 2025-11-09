from __future__ import annotations

from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import Field, HttpUrl, StringConstraints

from app.base import ORMModel

# Type aliases for reference fields
NAME_64 = Annotated[str, StringConstraints(min_length=1, max_length=64)]
NAME_128 = Annotated[str, StringConstraints(min_length=1, max_length=128)]
NAME_32 = Annotated[str, StringConstraints(min_length=1, max_length=32)]
NAME_255 = Annotated[str, StringConstraints(min_length=1, max_length=255)]
CODE_2 = Annotated[str, StringConstraints(min_length=2, max_length=2)]
CODE_UNIQUE = Annotated[str, StringConstraints(min_length=1, max_length=50)]
URL_FIELD = Annotated[HttpUrl | None, Field(max_length=2048)]


# Tags schemas
class TagsBase(ORMModel):
    """Base schema for tags"""

    name: NAME_64
    code: CODE_UNIQUE
    category_id: UUID | None = None


class TagsCreate(TagsBase):
    """Schema for creating tags"""

    pass


class TagsUpdate(ORMModel):
    """Schema for updating tags"""

    name: NAME_64 | None = None
    code: CODE_UNIQUE | None = None
    category_id: UUID | None = None


class TagsRead(TagsBase):
    """Schema for reading tags"""

    id: UUID
    created_at: datetime
    updated_at: datetime


# Genres schemas
class GenresBase(ORMModel):
    """Base schema for genres"""

    name: NAME_64


class GenresCreate(GenresBase):
    """Schema for creating genres"""

    pass


class GenresUpdate(ORMModel):
    """Schema for updating genres"""

    name: NAME_64 | None = None


class GenresRead(GenresBase):
    """Schema for reading genres"""

    id: UUID
    created_at: datetime
    updated_at: datetime


# Country schemas
class CountryBase(ORMModel):
    """Base schema for countries"""

    name: NAME_64
    code: CODE_2


class CountryCreate(CountryBase):
    """Schema for creating countries"""

    pass


class CountryUpdate(ORMModel):
    """Schema for updating countries"""

    name: NAME_64 | None = None
    code: CODE_2 | None = None


class CountryRead(CountryBase):
    """Schema for reading countries"""

    id: UUID
    created_at: datetime
    updated_at: datetime


# Language schemas
class LanguageBase(ORMModel):
    """Base schema for languages"""

    name: NAME_64
    code: CODE_2


class LanguageCreate(LanguageBase):
    """Schema for creating languages"""

    pass


class LanguageUpdate(ORMModel):
    """Schema for updating languages"""

    name: NAME_64 | None = None
    code: CODE_2 | None = None


class LanguageRead(LanguageBase):
    """Schema for reading languages"""

    id: int
    created_at: datetime
    updated_at: datetime


# Author schemas
class AuthorBase(ORMModel):
    """Base schema for authors"""

    full_name: NAME_128
    link: URL_FIELD = None


class AuthorCreate(AuthorBase):
    """Schema for creating authors"""

    pass


class AuthorUpdate(ORMModel):
    """Schema for updating authors"""

    full_name: NAME_128 | None = None
    link: URL_FIELD = None


class AuthorRead(AuthorBase):
    """Schema for reading authors"""

    id: int
    created_at: datetime
    updated_at: datetime


# Platform schemas
class PlatformBase(ORMModel):
    """Base schema for platforms"""

    name: NAME_64


class PlatformCreate(PlatformBase):
    """Schema for creating platforms"""

    pass


class PlatformUpdate(ORMModel):
    """Schema for updating platforms"""

    name: NAME_64 | None = None


class PlatformRead(PlatformBase):
    """Schema for reading platforms"""

    id: int
    created_at: datetime
    updated_at: datetime


# AgeRating schemas
class AgeRatingBase(ORMModel):
    """Base schema for age ratings"""

    name: NAME_32
    value: NAME_32
    description: NAME_255


class AgeRatingCreate(AgeRatingBase):
    """Schema for creating age ratings"""

    pass


class AgeRatingUpdate(ORMModel):
    """Schema for updating age ratings"""

    name: NAME_32 | None = None
    value: NAME_32 | None = None
    description: NAME_255 | None = None


class AgeRatingRead(AgeRatingBase):
    """Schema for reading age ratings"""

    id: int
    created_at: datetime
    updated_at: datetime


# DifficultyLevel schemas
class DifficultyLevelBase(ORMModel):
    """Base schema for difficulty levels"""

    name: NAME_32
    level: int = Field(..., ge=1)
    description: NAME_255


class DifficultyLevelCreate(DifficultyLevelBase):
    """Schema for creating difficulty levels"""

    pass


class DifficultyLevelUpdate(ORMModel):
    """Schema for updating difficulty levels"""

    name: NAME_32 | None = None
    level: int | None = Field(None, ge=1)
    description: NAME_255 | None = None


class DifficultyLevelRead(DifficultyLevelBase):
    """Schema for reading difficulty levels"""

    id: int
    created_at: datetime
    updated_at: datetime


# ContentCategory schemas
class ContentCategoryBase(ORMModel):
    """Base schema for content categories"""

    name: NAME_64
    description: NAME_255 | None = None
    is_active: bool = Field(default=True)
    sort_order: int = Field(default=0, ge=0)


class ContentCategoryCreate(ContentCategoryBase):
    """Schema for creating content categories"""

    pass


class ContentCategoryUpdate(ORMModel):
    """Schema for updating content categories"""

    name: NAME_64 | None = None
    description: NAME_255 | None = None
    is_active: bool | None = None
    sort_order: int | None = Field(None, ge=0)


class ContentCategoryRead(ContentCategoryBase):
    """Schema for reading content categories"""

    id: UUID
    created_at: datetime
    updated_at: datetime
