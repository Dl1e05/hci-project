from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.references.models import Platform
from app.references.schemas import PlatformCreate, PlatformRead, PlatformUpdate


class PlatformService:
    @staticmethod
    async def create(db: AsyncSession, platform_data: PlatformCreate) -> PlatformRead:
        platform = Platform(**platform_data.model_dump())
        db.add(platform)
        await db.commit()
        await db.refresh(platform)
        return PlatformRead.model_validate(platform)

    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[PlatformRead]:
        result = await db.execute(select(Platform).offset(skip).limit(limit).order_by(Platform.name))
        platforms = result.scalars().all()
        return [PlatformRead.model_validate(platform) for platform in platforms]

    @staticmethod
    async def get_by_id(db: AsyncSession, platform_id: int) -> PlatformRead | None:
        result = await db.execute(select(Platform).where(Platform.id == platform_id))
        platform = result.scalar_one_or_none()
        return PlatformRead.model_validate(platform) if platform else None

    @staticmethod
    async def get_by_name(db: AsyncSession, name: str) -> Platform | None:
        result = await db.execute(select(Platform).where(Platform.name == name))
        return result.scalar_one_or_none()

    @staticmethod
    async def update(db: AsyncSession, platform_id: int, platform_data: PlatformUpdate) -> PlatformRead | None:
        result = await db.execute(select(Platform).where(Platform.id == platform_id))
        platform_entity = result.scalar_one_or_none()
        if not platform_entity:
            return None

        update_data = platform_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(platform_entity, field, value)

        await db.commit()
        await db.refresh(platform_entity)
        return PlatformRead.model_validate(platform_entity)

    @staticmethod
    async def delete(db: AsyncSession, platform_id: int) -> bool:
        result = await db.execute(select(Platform).where(Platform.id == platform_id))
        platform_entity = result.scalar_one_or_none()
        if not platform_entity:
            return False

        await db.delete(platform_entity)
        await db.commit()
        return True

