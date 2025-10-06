import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.base import Base

if TYPE_CHECKING:
    pass

# Промежуточная таблица для Many-to-Many связи
content_type_tags = Table(
    'content_type_tags',
    Base.metadata,
    Column('content_type_id', PG_UUID(as_uuid=True), ForeignKey('content_types.id', ondelete='CASCADE'), primary_key=True),
    Column('tag_id', PG_UUID(as_uuid=True), ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
)


class Tags(Base):
    """Модель тегов"""
    __tablename__ = "tags"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    code: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)

    # Обратная связь с ContentType
    content_types: Mapped[list["ContentType"]] = relationship(
        "ContentType",
        secondary=content_type_tags,
        back_populates="tags"
    )


class ContentType(Base):
    """Модель типов контента"""
    __tablename__ = "content_types"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    order: Mapped[int] = mapped_column(Integer, nullable=False, index=True)

    # Связь с Tags
    tags: Mapped[list["Tags"]] = relationship(
        "Tags",
        secondary=content_type_tags,
        back_populates="content_types"
    )
