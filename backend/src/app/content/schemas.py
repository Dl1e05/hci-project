from uuid import UUID

from pydantic import BaseModel, Field


class TagsBase(BaseModel):
    name: str
    code: str

class TagsCreate(TagsBase):
    pass

class TagsUpdate(BaseModel):
    name: str | None = None
    code: str | None = None

class TagsRead(TagsBase):
    id: UUID

    model_config = {"from_attributes": True}

"""------------------------------------------------------------------------"""

class ContentTypeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    order: int = Field(..., ge=1)


class ContentTypeCreate(ContentTypeBase):
    tag_ids: list[UUID] = Field(default_factory=list)


class ContentTypeUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    order: int | None = Field(None, ge=1)
    tag_ids: list[UUID] | None = None


class ContentTypeRead(ContentTypeBase):
    id: UUID
    tags: list[TagsRead] = Field(default_factory=list)

    class Config:
        from_attributes = True