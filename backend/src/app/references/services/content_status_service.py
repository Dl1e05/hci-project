from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.references.models import ContentStatus
from app.references.schemas import ContentStatusCreate, ContentStatusRead, ContentStatusUpdate


class ContentStatusService:
    @staticmethod
    async def create(db: AsyncSession, status_data: ContentStatusCreate) -> ContentStatusRead:
        status = ContentStatus(**status_data.model_dump())
        db.add(status)
        await db.commit()
        await db.refresh(status)
        return ContentStatusRead.model_validate(status)

    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[ContentStatusRead]:
        result = await db.execute(select(ContentStatus).offset(skip).limit(limit).order_by(ContentStatus.name))
        statuses = result.scalars().all()
        return [ContentStatusRead.model_validate(status) for status in statuses]

    @staticmethod
    async def get_by_id(db: AsyncSession, status_id: int) -> ContentStatusRead | None:
        result = await db.execute(select(ContentStatus).where(ContentStatus.id == status_id))
        status = result.scalar_one_or_none()
        return ContentStatusRead.model_validate(status) if status else None

    @staticmethod
    async def get_by_name(db: AsyncSession, name: str) -> ContentStatus | None:
        result = await db.execute(select(ContentStatus).where(ContentStatus.name == name))
        return result.scalar_one_or_none()

    @staticmethod
    async def update(db: AsyncSession, status_id: int, status_data: ContentStatusUpdate) -> ContentStatusRead | None:
        result = await db.execute(select(ContentStatus).where(ContentStatus.id == status_id))
        status_entity = result.scalar_one_or_none()
        if not status_entity:
            return None

        update_data = status_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(status_entity, field, value)

        await db.commit()
        await db.refresh(status_entity)
        return ContentStatusRead.model_validate(status_entity)

    @staticmethod
    async def delete(db: AsyncSession, status_id: int) -> bool:
        result = await db.execute(select(ContentStatus).where(ContentStatus.id == status_id))
        status_entity = result.scalar_one_or_none()
        if not status_entity:
            return False

        await db.delete(status_entity)
        await db.commit()
        return True

