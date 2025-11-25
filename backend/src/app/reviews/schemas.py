from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import Field, StringConstraints

from app.base import ORMModel

COMMENTARY = Annotated[str, StringConstraints(min_length=1, max_length=5000)]


class ReviewCreate(ORMModel):
    content_id: UUID
    user_id: UUID
    commentary: COMMENTARY
    users_difficulty_level: int = Field(..., ge=1)


class ReviewUpdate(ORMModel):
    commentary: COMMENTARY | None = None
    users_difficulty_level: int | None = Field(None, ge=1)


class ReviewRead(ORMModel):
    id: UUID
    content_id: UUID
    user_id: UUID
    commentary: str
    users_difficulty_level: int
    created_at: datetime
    updated_at: datetime
