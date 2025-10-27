from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.content.models.content import Podcast
from app.content.repo import ContentRepository
from app.content.schemas.content import PodcastCreate, PodcastRead, PodcastUpdate


class PodcastService:
    @staticmethod
    async def create(db: AsyncSession, podcast_data: PodcastCreate) -> PodcastRead:
        data = podcast_data.model_dump()
        podcast = await ContentRepository.create(db, Podcast, data)
        return PodcastRead.model_validate(podcast)

    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[PodcastRead]:
        podcasts = await ContentRepository.get_all(db, Podcast, skip, limit)
        return [PodcastRead.model_validate(podcast) for podcast in podcasts]

    @staticmethod
    async def get_by_id(db: AsyncSession, podcast_id: UUID) -> PodcastRead | None:
        podcast = await ContentRepository.get_by_id(db, Podcast, podcast_id)
        return PodcastRead.model_validate(podcast) if podcast else None

    @staticmethod
    async def update(db: AsyncSession, podcast_id: UUID, podcast_data: PodcastUpdate) -> PodcastRead | None:
        data = podcast_data.model_dump(exclude_unset=True)
        podcast = await ContentRepository.update(db, Podcast, podcast_id, data)
        return PodcastRead.model_validate(podcast) if podcast else None

    @staticmethod
    async def delete(db: AsyncSession, podcast_id: UUID) -> bool:
        return await ContentRepository.delete(db, Podcast, podcast_id)

