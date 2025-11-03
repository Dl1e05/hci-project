from __future__ import annotations

from datetime import datetime
from typing import Annotated
from uuid import UUID
from pydantic import Field, StringConstraints, HttpUrl
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


class TagsCreate(TagsBase):
    """Schema for creating tags"""
    pass


class TagsUpdate(ORMModel):
    """Schema for updating tags"""
    name: NAME_64 | None = None
    code: CODE_UNIQUE | None = None


class TagsRead(TagsBase):
    """Schema for reading tags"""
    id: UUID
    created_at: datetime
    updated_at: datetime


# ContentType schemas
class ContentTypeBase(ORMModel):
    """Base schema for content types"""
    name: NAME_64
    order: int = Field(..., ge=1)


class ContentTypeCreate(ContentTypeBase):
    """Schema for creating content types"""
    tag_ids: list[UUID] = Field(default_factory=list)


class ContentTypeUpdate(ORMModel):
    """Schema for updating content types"""
    name: NAME_64 | None = None
    order: int | None = Field(None, ge=1)
    tag_ids: list[UUID] | None = None


class ContentTypeRead(ContentTypeBase):
    """Schema for reading content types"""
    id: UUID
    tags: list[TagsRead] = Field(default_factory=list)
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
    min_score: float = Field(..., ge=0.0)
    max_score: float = Field(..., ge=0.0)


class DifficultyLevelCreate(DifficultyLevelBase):
    """Schema for creating difficulty levels"""
    pass


class DifficultyLevelUpdate(ORMModel):
    """Schema for updating difficulty levels"""
    name: NAME_32 | None = None
    level: int | None = Field(None, ge=1)
    description: NAME_255 | None = None
    min_score: float | None = Field(None, ge=0.0)
    max_score: float | None = Field(None, ge=0.0)


class DifficultyLevelRead(DifficultyLevelBase):
    """Schema for reading difficulty levels"""
    id: int
    created_at: datetime
    updated_at: datetime


# ContentStatus schemas
class ContentStatusBase(ORMModel):
    """Base schema for content statuses"""
    name: NAME_32
    description: NAME_255 | None = None


class ContentStatusCreate(ContentStatusBase):
    """Schema for creating content statuses"""
    pass


class ContentStatusUpdate(ORMModel):
    """Schema for updating content statuses"""
    name: NAME_32 | None = None
    description: NAME_255 | None = None


class ContentStatusRead(ContentStatusBase):
    """Schema for reading content statuses"""
    id: int
    created_at: datetime
    updated_at: datetime


# ContentCategory schemas
class ContentCategoryBase(ORMModel):
    """Base schema for content categories"""
    name: NAME_64
    description: NAME_255 | None = None
    parent_id: UUID | None = None
    is_active: bool = Field(default=True)
    sort_order: int = Field(default=0, ge=0)


class ContentCategoryCreate(ContentCategoryBase):
    """Schema for creating content categories"""
    pass


class ContentCategoryUpdate(ORMModel):
    """Schema for updating content categories"""
    name: NAME_64 | None = None
    description: NAME_255 | None = None
    parent_id: UUID | None = None
    is_active: bool | None = None
    sort_order: int | None = Field(None, ge=0)


class ContentCategoryRead(ContentCategoryBase):
    """Schema for reading content categories"""
    id: UUID
    parent: "ContentCategoryRead | None" = None
    children: list["ContentCategoryRead"] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
