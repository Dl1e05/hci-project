from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.references.models import Genres
from app.references.schemas import GenresCreate, GenresRead, GenresUpdate


class GenresService:
    @staticmethod
    async def create(db: AsyncSession, genre_data: GenresCreate) -> GenresRead:
        genre = Genres(**genre_data.model_dump())
        db.add(genre)
        await db.commit()
        await db.refresh(genre)
        return GenresRead.model_validate(genre)

    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[GenresRead]:
        result = await db.execute(select(Genres).offset(skip).limit(limit).order_by(Genres.name))
        genres = result.scalars().all()
        return [GenresRead.model_validate(genre) for genre in genres]

    @staticmethod
    async def get_by_id(db: AsyncSession, genre_id: UUID) -> GenresRead | None:
        result = await db.execute(select(Genres).where(Genres.id == genre_id))
        genre = result.scalar_one_or_none()
        return GenresRead.model_validate(genre) if genre else None

    @staticmethod
    async def get_by_name(db: AsyncSession, name: str) -> Genres | None:
        result = await db.execute(select(Genres).where(Genres.name == name))
        return result.scalar_one_or_none()

    @staticmethod
    async def update(db: AsyncSession, genre_id: UUID, genre_data: GenresUpdate) -> GenresRead | None:
        result = await db.execute(select(Genres).where(Genres.id == genre_id))
        genre_entity = result.scalar_one_or_none()
        if not genre_entity:
            return None

        update_data = genre_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(genre_entity, field, value)

        await db.commit()
        await db.refresh(genre_entity)
        return GenresRead.model_validate(genre_entity)

    @staticmethod
    async def delete(db: AsyncSession, genre_id: UUID) -> bool:
        result = await db.execute(select(Genres).where(Genres.id == genre_id))
        genre_entity = result.scalar_one_or_none()
        if not genre_entity:
            return False

        await db.delete(genre_entity)
        await db.commit()
        return True

