from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.content.models.content import Video
from app.content.repo import ContentRepository
from app.content.schemas.content import VideoCreate, VideoRead, VideoUpdate


class VideoService:
    @staticmethod
    async def create(db: AsyncSession, video_data: VideoCreate) -> VideoRead:
        data = video_data.model_dump()
        video = await ContentRepository.create(db, Video, data)
        return VideoRead.model_validate(video)

    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[VideoRead]:
        videos = await ContentRepository.get_all(db, Video, skip, limit)
        return [VideoRead.model_validate(video) for video in videos]

    @staticmethod
    async def get_by_id(db: AsyncSession, video_id: UUID) -> VideoRead | None:
        video = await ContentRepository.get_by_id(db, Video, video_id)
        return VideoRead.model_validate(video) if video else None

    @staticmethod
    async def update(db: AsyncSession, video_id: UUID, video_data: VideoUpdate) -> VideoRead | None:
        data = video_data.model_dump(exclude_unset=True)
        video = await ContentRepository.update(db, Video, video_id, data)
        return VideoRead.model_validate(video) if video else None

    @staticmethod
    async def delete(db: AsyncSession, video_id: UUID) -> bool:
        return await ContentRepository.delete(db, Video, video_id)

