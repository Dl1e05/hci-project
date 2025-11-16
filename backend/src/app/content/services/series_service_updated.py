from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.content.models.content import Series
from app.content.repo import ContentRepository
from app.content.schemas.content import SeriesCreate, SeriesRead, SeriesUpdate
from app.content.schemas.filters import SeriesFilterParams


class SeriesService:
    @staticmethod
    async def create(db: AsyncSession, series_data: SeriesCreate) -> SeriesRead:
        data = series_data.model_dump(mode='python')
        series = await ContentRepository.create(db, Series, data)
        return SeriesRead.model_validate(series)

    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[SeriesRead]:
        series_list = await ContentRepository.get_all(db, Series, skip, limit)
        return [SeriesRead.model_validate(series) for series in series_list]

    @staticmethod
    async def get_filtered(
        db: AsyncSession, filters: SeriesFilterParams, skip: int = 0, limit: int = 100
    ) -> tuple[list[SeriesRead], int]:
        """Get filtered series with pagination"""
        additional_filters = {}

        if filters.is_ongoing is not None:
            additional_filters['is_ongoing'] = filters.is_ongoing

        if filters.season is not None:
            additional_filters['season'] = filters.season

        if filters.min_episodes is not None or filters.max_episodes is not None:
            additional_filters['total_episodes'] = {}
            if filters.min_episodes is not None:
                additional_filters['total_episodes']['min'] = filters.min_episodes
            if filters.max_episodes is not None:
                additional_filters['total_episodes']['max'] = filters.max_episodes

        series_list, total = await ContentRepository.get_filtered(
            db, Series, filters, skip=skip, limit=limit, additional_filters=additional_filters
        )

        return [SeriesRead.model_validate(series) for series in series_list], total

    @staticmethod
    async def get_by_id(db: AsyncSession, series_id: UUID) -> SeriesRead | None:
        series = await ContentRepository.get_by_id(db, Series, series_id)
        return SeriesRead.model_validate(series) if series else None

    @staticmethod
    async def update(db: AsyncSession, series_id: UUID, series_data: SeriesUpdate) -> SeriesRead | None:
        data = series_data.model_dump(exclude_unset=True, mode='python')
        series = await ContentRepository.update(db, Series, series_id, data)
        return SeriesRead.model_validate(series) if series else None

    @staticmethod
    async def delete(db: AsyncSession, series_id: UUID) -> bool:
        return await ContentRepository.delete(db, Series, series_id)
