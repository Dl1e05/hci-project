from uuid import UUID
from pydantic import BaseModel, Field
from enum import Enum


class WatchStatusEnum(str, Enum):
    COMPLETED = "completed"
    PLANNED = "planned"
    DROPPED = "dropped"


class UserContentListCreate(BaseModel):
    status: WatchStatusEnum = WatchStatusEnum.PLANNED


class UserContentListUpdate(BaseModel):
    status: WatchStatusEnum | None = None


class UserContentListRead(BaseModel):
    id: UUID
    user_id: UUID
    content_id: UUID
    status: WatchStatusEnum

    class Config:
        from_attributes = True


class UserContentListReadStats(BaseModel):
    completed_count: int
    planned_count: int
    dropped_count: int


class UserContentListReadGroups(BaseModel):
    completed: list[UserContentListRead] = Field(default_factory=list)
    planned: list[UserContentListRead] = Field(default_factory=list)
    dropped: list[UserContentListRead] = Field(default_factory=list)
