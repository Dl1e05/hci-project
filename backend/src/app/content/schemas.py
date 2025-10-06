from uuid import UUID

from pydantic import BaseModel, Field, PositiveInt


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

    class Config:
        orm_mode = True

"""------------------------------------------------------------------------"""

class ContentTypeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    order: PositiveInt = Field(..., gt=0)


class ContentTypeCreate(ContentTypeBase):
    tag_ids: list[UUID] = Field(default_factory=list)


class ContentTypeUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    order: PositiveInt | None = Field(None, gt=0)
    tag_ids: list[UUID] | None = None


class ContentTypeRead(ContentTypeBase):
    id: UUID
    tags: list[TagsRead] = Field(default_factory=list)

    class Config:
        from_attributes = True