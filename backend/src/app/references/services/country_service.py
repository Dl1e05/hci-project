from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.references.models import Country
from app.references.schemas import CountryCreate, CountryRead, CountryUpdate


class CountryService:
    @staticmethod
    async def create(db: AsyncSession, country_data: CountryCreate) -> CountryRead:
        country = Country(**country_data.model_dump())
        db.add(country)
        await db.commit()
        await db.refresh(country)
        return CountryRead.model_validate(country)

    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[CountryRead]:
        result = await db.execute(select(Country).offset(skip).limit(limit).order_by(Country.name))
        countries = result.scalars().all()
        return [CountryRead.model_validate(country) for country in countries]

    @staticmethod
    async def get_by_id(db: AsyncSession, country_id: UUID) -> CountryRead | None:
        result = await db.execute(select(Country).where(Country.id == country_id))
        country = result.scalar_one_or_none()
        return CountryRead.model_validate(country) if country else None

    @staticmethod
    async def get_by_code(db: AsyncSession, code: str) -> Country | None:
        result = await db.execute(select(Country).where(Country.code == code))
        return result.scalar_one_or_none()

    @staticmethod
    async def update(db: AsyncSession, country_id: UUID, country_data: CountryUpdate) -> CountryRead | None:
        result = await db.execute(select(Country).where(Country.id == country_id))
        country_entity = result.scalar_one_or_none()
        if not country_entity:
            return None

        update_data = country_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(country_entity, field, value)

        await db.commit()
        await db.refresh(country_entity)
        return CountryRead.model_validate(country_entity)

    @staticmethod
    async def delete(db: AsyncSession, country_id: UUID) -> bool:
        result = await db.execute(select(Country).where(Country.id == country_id))
        country_entity = result.scalar_one_or_none()
        if not country_entity:
            return False

        await db.delete(country_entity)
        await db.commit()
        return True

