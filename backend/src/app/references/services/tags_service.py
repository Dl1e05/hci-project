from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.references.models import Tags
from app.references.schemas import TagsCreate, TagsRead, TagsUpdate


class TagsService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    @staticmethod
    async def create(db: AsyncSession, tag_data: TagsCreate) -> TagsRead:
        tag = Tags(**tag_data.model_dump())
        db.add(tag)
        await db.commit()
        await db.refresh(tag)
        return TagsRead.model_validate(tag)

    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[TagsRead]:
        result = await db.execute(select(Tags).options(selectinload(Tags.content_types)).offset(skip).limit(limit))
        tags = result.scalars().all()
        return [TagsRead.model_validate(tag) for tag in tags]

    @staticmethod
    async def get_by_id(db: AsyncSession, tag_id: UUID) -> TagsRead | None:
        result = await db.execute(select(Tags).options(selectinload(Tags.content_types)).where(Tags.id == tag_id))
        tag = result.scalar_one_or_none()
        return TagsRead.model_validate(tag) if tag else None

    @staticmethod
    async def get_by_code(db: AsyncSession, code: str) -> Tags | None:
        result = await db.execute(select(Tags).where(Tags.code == code))
        return result.scalar_one_or_none()

    @staticmethod
    async def update(db: AsyncSession, tag_id: UUID, tag_data: TagsUpdate) -> TagsRead | None:
        # Fetch ORM entity, not Pydantic schema
        result = await db.execute(select(Tags).where(Tags.id == tag_id))
        tag_entity = result.scalar_one_or_none()
        if not tag_entity:
            return None

        update_data = tag_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(tag_entity, field, value)

        await db.commit()
        await db.refresh(tag_entity)
        return TagsRead.model_validate(tag_entity)

    @staticmethod
    async def delete(db: AsyncSession, tag_id: UUID) -> bool:
        # Fetch ORM entity, not Pydantic schema
        result = await db.execute(select(Tags).where(Tags.id == tag_id))
        tag_entity = result.scalar_one_or_none()
        if not tag_entity:
            return False

        await db.delete(tag_entity)
        await db.commit()
        return True
