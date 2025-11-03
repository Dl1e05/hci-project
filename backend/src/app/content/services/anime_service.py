from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.content.models.content import Anime
from app.content.repo import ContentRepository
from app.content.schemas.content import AnimeCreate, AnimeRead, AnimeUpdate


class AnimeService:
    @staticmethod
    async def create(db: AsyncSession, anime_data: AnimeCreate) -> AnimeRead:
        data = anime_data.model_dump()
        anime = await ContentRepository.create(db, Anime, data)
        return AnimeRead.model_validate(anime)

    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[AnimeRead]:
        animes = await ContentRepository.get_all(db, Anime, skip, limit)
        return [AnimeRead.model_validate(anime) for anime in animes]

    @staticmethod
    async def get_by_id(db: AsyncSession, anime_id: UUID) -> AnimeRead | None:
        anime = await ContentRepository.get_by_id(db, Anime, anime_id)
        return AnimeRead.model_validate(anime) if anime else None

    @staticmethod
    async def update(db: AsyncSession, anime_id: UUID, anime_data: AnimeUpdate) -> AnimeRead | None:
        data = anime_data.model_dump(exclude_unset=True)
        anime = await ContentRepository.update(db, Anime, anime_id, data)
        return AnimeRead.model_validate(anime) if anime else None

    @staticmethod
    async def delete(db: AsyncSession, anime_id: UUID) -> bool:
        return await ContentRepository.delete(db, Anime, anime_id)

