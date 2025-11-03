from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.content.models.content import Film
from app.content.repo import ContentRepository
from app.content.schemas.content import FilmCreate, FilmRead, FilmUpdate


class FilmService:
    @staticmethod
    async def create(db: AsyncSession, film_data: FilmCreate) -> FilmRead:
        data = film_data.model_dump()
        film = await ContentRepository.create(db, Film, data)
        return FilmRead.model_validate(film)

    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[FilmRead]:
        films = await ContentRepository.get_all(db, Film, skip, limit)
        return [FilmRead.model_validate(film) for film in films]

    @staticmethod
    async def get_by_id(db: AsyncSession, film_id: UUID) -> FilmRead | None:
        film = await ContentRepository.get_by_id(db, Film, film_id)
        return FilmRead.model_validate(film) if film else None

    @staticmethod
    async def update(db: AsyncSession, film_id: UUID, film_data: FilmUpdate) -> FilmRead | None:
        data = film_data.model_dump(exclude_unset=True)
        film = await ContentRepository.update(db, Film, film_id, data)
        return FilmRead.model_validate(film) if film else None

    @staticmethod
    async def delete(db: AsyncSession, film_id: UUID) -> bool:
        return await ContentRepository.delete(db, Film, film_id)

