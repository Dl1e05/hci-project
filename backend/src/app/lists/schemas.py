from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

class ContentTypeEnum(str, Enum):
    MEDIA = "media"
    GAMES = "games"
    LITERATURE = "literature"

class WatchStatusEnum(str, Enum):
    COMPLETED = "completed"
    PLANNED = "planned"
    DROPPED = "dropped"
    WATCHING = "watching"
    POSTPONED = "postponed"

    READ = "read"
    READING = "reading"

    FINISHED = "finished"
    PLAYING = "playing"

VALID_STATUS_COMBINATIONS = {
    ContentTypeEnum.MEDIA: {
        WatchStatusEnum.COMPLETED,
        WatchStatusEnum.PLANNED,
        WatchStatusEnum.DROPPED,
        WatchStatusEnum.WATCHING,
        WatchStatusEnum.POSTPONED,
    },
    ContentTypeEnum.GAMES: {
        WatchStatusEnum.FINISHED,
        WatchStatusEnum.PLAYING,
        WatchStatusEnum.PLANNED,
        WatchStatusEnum.DROPPED,
        WatchStatusEnum.POSTPONED,
    },
    ContentTypeEnum.LITERATURE: {
        WatchStatusEnum.READ,
        WatchStatusEnum.READING,
        WatchStatusEnum.PLANNED,
        WatchStatusEnum.DROPPED,
        WatchStatusEnum.POSTPONED,
    },
}

class UserContentListCreate(BaseModel):
    content_type: ContentTypeEnum
    status: WatchStatusEnum = WatchStatusEnum.PLANNED
    
    @field_validator('status')
    @classmethod
    def validate_status_for_content_type(cls, status: WatchStatusEnum, info) -> WatchStatusEnum:
        content_type = info.data.get('content_type')
        if content_type and status not in VALID_STATUS_COMBINATIONS.get(content_type, set()):
            raise ValueError(
                f"Status '{status.value}' is not valid for content type '{content_type.value}'. "
                f"Valid statuses: {[s.value for s in VALID_STATUS_COMBINATIONS[content_type]]}"
            )
        return status

class UserContentListUpdate(BaseModel):
    status: WatchStatusEnum | None = None


class UserContentListRead(BaseModel):
    id: UUID
    user_id: UUID
    content_id: UUID
    content_type: ContentTypeEnum
    status: WatchStatusEnum

    class Config:
        from_attributes = True


class UserContentListReadStats(BaseModel):
    completed_count: int
    planned_count: int
    dropped_count: int
    watching_count: int
    postponed_count: int
    
    read_count: int
    reading_count: int
    
    finished_count: int
    playing_count: int

class UserContentListReadGroups(BaseModel):
    completed: list[UserContentListRead] = Field(default_factory=list)
    planned: list[UserContentListRead] = Field(default_factory=list)
    dropped: list[UserContentListRead] = Field(default_factory=list)
    watching: list[UserContentListRead] = Field(default_factory=list)
    postponed: list[UserContentListRead] = Field(default_factory=list)

    read: list[UserContentListRead] = Field(default_factory=list)
    reading: list[UserContentListRead] = Field(default_factory=list)
    
    finished: list[UserContentListRead] = Field(default_factory=list)
    playing: list[UserContentListRead] = Field(default_factory=list)