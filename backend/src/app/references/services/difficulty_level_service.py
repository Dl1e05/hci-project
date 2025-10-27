from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.references.models import DifficultyLevel
from app.references.schemas import DifficultyLevelCreate, DifficultyLevelRead, DifficultyLevelUpdate


class DifficultyLevelService:
    @staticmethod
    async def create(db: AsyncSession, difficulty_data: DifficultyLevelCreate) -> DifficultyLevelRead:
        difficulty = DifficultyLevel(**difficulty_data.model_dump())
        db.add(difficulty)
        await db.commit()
        await db.refresh(difficulty)
        return DifficultyLevelRead.model_validate(difficulty)

    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[DifficultyLevelRead]:
        result = await db.execute(select(DifficultyLevel).offset(skip).limit(limit).order_by(DifficultyLevel.level))
        difficulties = result.scalars().all()
        return [DifficultyLevelRead.model_validate(difficulty) for difficulty in difficulties]

    @staticmethod
    async def get_by_id(db: AsyncSession, difficulty_id: int) -> DifficultyLevelRead | None:
        result = await db.execute(select(DifficultyLevel).where(DifficultyLevel.id == difficulty_id))
        difficulty = result.scalar_one_or_none()
        return DifficultyLevelRead.model_validate(difficulty) if difficulty else None

    @staticmethod
    async def get_by_level(db: AsyncSession, level: int) -> DifficultyLevel | None:
        result = await db.execute(select(DifficultyLevel).where(DifficultyLevel.level == level))
        return result.scalar_one_or_none()

    @staticmethod
    async def update(db: AsyncSession, difficulty_id: int, difficulty_data: DifficultyLevelUpdate) -> DifficultyLevelRead | None:
        result = await db.execute(select(DifficultyLevel).where(DifficultyLevel.id == difficulty_id))
        difficulty_entity = result.scalar_one_or_none()
        if not difficulty_entity:
            return None

        update_data = difficulty_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(difficulty_entity, field, value)

        await db.commit()
        await db.refresh(difficulty_entity)
        return DifficultyLevelRead.model_validate(difficulty_entity)

    @staticmethod
    async def delete(db: AsyncSession, difficulty_id: int) -> bool:
        result = await db.execute(select(DifficultyLevel).where(DifficultyLevel.id == difficulty_id))
        difficulty_entity = result.scalar_one_or_none()
        if not difficulty_entity:
            return False

        await db.delete(difficulty_entity)
        await db.commit()
        return True

