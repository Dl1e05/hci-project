from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.references.models import ContentCategory
from app.references.schemas import ContentCategoryCreate, ContentCategoryRead, ContentCategoryUpdate


class ContentCategoryService:
    @staticmethod
    async def create(db: AsyncSession, category_data: ContentCategoryCreate) -> ContentCategoryRead:
        category = ContentCategory(**category_data.model_dump())
        db.add(category)
        await db.commit()
        await db.refresh(category)
        return ContentCategoryRead.model_validate(category)

    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[ContentCategoryRead]:
        result = await db.execute(
            select(ContentCategory)
            .options(selectinload(ContentCategory.parent), selectinload(ContentCategory.children))
            .offset(skip)
            .limit(limit)
            .order_by(ContentCategory.sort_order)
        )
        categories = result.scalars().all()
        return [ContentCategoryRead.model_validate(category) for category in categories]

    @staticmethod
    async def get_by_id(db: AsyncSession, category_id: UUID) -> ContentCategoryRead | None:
        result = await db.execute(
            select(ContentCategory)
            .options(selectinload(ContentCategory.parent), selectinload(ContentCategory.children))
            .where(ContentCategory.id == category_id)
        )
        category = result.scalar_one_or_none()
        return ContentCategoryRead.model_validate(category) if category else None

    @staticmethod
    async def get_by_name(db: AsyncSession, name: str) -> ContentCategory | None:
        result = await db.execute(select(ContentCategory).where(ContentCategory.name == name))
        return result.scalar_one_or_none()

    @staticmethod
    async def update(db: AsyncSession, category_id: UUID, category_data: ContentCategoryUpdate) -> ContentCategoryRead | None:
        result = await db.execute(
            select(ContentCategory)
            .options(selectinload(ContentCategory.parent), selectinload(ContentCategory.children))
            .where(ContentCategory.id == category_id)
        )
        category_entity = result.scalar_one_or_none()
        if not category_entity:
            return None

        update_data = category_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(category_entity, field, value)

        await db.commit()
        await db.refresh(category_entity, attribute_names=['parent', 'children'])
        return ContentCategoryRead.model_validate(category_entity)

    @staticmethod
    async def delete(db: AsyncSession, category_id: UUID) -> bool:
        result = await db.execute(select(ContentCategory).where(ContentCategory.id == category_id))
        category_entity = result.scalar_one_or_none()
        if not category_entity:
            return False

        await db.delete(category_entity)
        await db.commit()
        return True

