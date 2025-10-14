from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.content.models import ContentType, Tags
from app.content.schemas import ContentTypeCreate, ContentTypeRead, ContentTypeUpdate


class ContentTypesService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    @staticmethod
    async def create(db: AsyncSession, content_type_data: ContentTypeCreate) -> ContentTypeRead:
        data_dict = content_type_data.model_dump(exclude={'tag_ids'})
        content_type = ContentType(**data_dict)

        if content_type_data.tag_ids:
            result = await db.execute(select(Tags).where(Tags.id.in_(content_type_data.tag_ids)))
            tags: list[Tags] = list(result.scalars().all())
            content_type.tags = tags

        db.add(content_type)
        await db.commit()
        await db.refresh(content_type, attribute_names=['tags'])
        return ContentTypeRead.model_validate(content_type)

    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[ContentTypeRead]:
        result = await db.execute(
            select(ContentType).options(selectinload(ContentType.tags)).offset(skip).limit(limit).order_by(ContentType.order)
        )
        content = result.scalars().all()
        return [ContentTypeRead.model_validate(ct) for ct in content]

    @staticmethod
    async def get_by_id(db: AsyncSession, content_type_id: UUID) -> ContentTypeRead | None:
        result = await db.execute(
            select(ContentType).options(selectinload(ContentType.tags)).where(ContentType.id == content_type_id)
        )
        content_type = result.scalar_one_or_none()
        return ContentTypeRead.model_validate(content_type) if content_type else None

    @staticmethod
    async def update(db: AsyncSession, content_type_id: UUID, content_type_data: ContentTypeUpdate) -> ContentTypeRead | None:
        result = await db.execute(
            select(ContentType).options(selectinload(ContentType.tags)).where(ContentType.id == content_type_id)
        )
        content_type_entity = result.scalar_one_or_none()
        if not content_type_entity:
            return None

        update_data = content_type_data.model_dump(exclude_unset=True, exclude={'tag_ids'})
        for field, value in update_data.items():
            setattr(content_type_entity, field, value)

        if content_type_data.tag_ids is not None:
            tags_result = await db.execute(select(Tags).where(Tags.id.in_(content_type_data.tag_ids)))
            tags: list[Tags] = list(tags_result.scalars().all())
            content_type_entity.tags = tags

        await db.commit()
        await db.refresh(content_type_entity, attribute_names=['tags'])
        return ContentTypeRead.model_validate(content_type_entity)

    @staticmethod
    async def delete(db: AsyncSession, content_type_id: UUID) -> bool:
        result = await db.execute(select(ContentType).where(ContentType.id == content_type_id))
        content_type_entity = result.scalar_one_or_none()
        if not content_type_entity:
            return False

        await db.delete(content_type_entity)
        await db.commit()
        return True
