from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.references.models import AgeRating
from app.references.schemas import AgeRatingCreate, AgeRatingRead, AgeRatingUpdate


class AgeRatingService:
    @staticmethod
    async def create(db: AsyncSession, age_rating_data: AgeRatingCreate) -> AgeRatingRead:
        age_rating = AgeRating(**age_rating_data.model_dump())
        db.add(age_rating)
        await db.commit()
        await db.refresh(age_rating)
        return AgeRatingRead.model_validate(age_rating)

    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[AgeRatingRead]:
        result = await db.execute(select(AgeRating).offset(skip).limit(limit).order_by(AgeRating.name))
        age_ratings = result.scalars().all()
        return [AgeRatingRead.model_validate(age_rating) for age_rating in age_ratings]

    @staticmethod
    async def get_by_id(db: AsyncSession, age_rating_id: int) -> AgeRatingRead | None:
        result = await db.execute(select(AgeRating).where(AgeRating.id == age_rating_id))
        age_rating = result.scalar_one_or_none()
        return AgeRatingRead.model_validate(age_rating) if age_rating else None

    @staticmethod
    async def get_by_value(db: AsyncSession, value: str) -> AgeRating | None:
        result = await db.execute(select(AgeRating).where(AgeRating.value == value))
        return result.scalar_one_or_none()

    @staticmethod
    async def update(db: AsyncSession, age_rating_id: int, age_rating_data: AgeRatingUpdate) -> AgeRatingRead | None:
        result = await db.execute(select(AgeRating).where(AgeRating.id == age_rating_id))
        age_rating_entity = result.scalar_one_or_none()
        if not age_rating_entity:
            return None

        update_data = age_rating_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(age_rating_entity, field, value)

        await db.commit()
        await db.refresh(age_rating_entity)
        return AgeRatingRead.model_validate(age_rating_entity)

    @staticmethod
    async def delete(db: AsyncSession, age_rating_id: int) -> bool:
        result = await db.execute(select(AgeRating).where(AgeRating.id == age_rating_id))
        age_rating_entity = result.scalar_one_or_none()
        if not age_rating_entity:
            return False

        await db.delete(age_rating_entity)
        await db.commit()
        return True

