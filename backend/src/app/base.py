from datetime import datetime

from pydantic import BaseModel, ConfigDict
from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# Must be inherited by all models
class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
    pass


# Must be inherited by all pydantic models
class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra='forbid')
