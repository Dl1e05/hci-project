from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED

from app.content.schemas.content import SeriesCreate, SeriesRead, SeriesUpdate
from app.content.services.series_service import SeriesService
from app.core.db import get_async_session

router = APIRouter(prefix='/content')


@router.post('/series', response_model=SeriesRead, status_code=HTTP_201_CREATED, tags=['series'])
async def create_series(series_data: SeriesCreate, db: AsyncSession = Depends(get_async_session)) -> SeriesRead:
    try:
        return await SeriesService.create(db, series_data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.get('/series', response_model=list[SeriesRead], tags=['series'])
async def get_all_series(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_session)) -> list[SeriesRead]:
    return await SeriesService.get_all(db, skip=skip, limit=limit)


@router.get('/series/{series_id}', response_model=SeriesRead, tags=['series'])
async def get_series(series_id: UUID, db: AsyncSession = Depends(get_async_session)) -> SeriesRead:
    series = await SeriesService.get_by_id(db, series_id)
    if not series:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Series with id {series_id} not found')
    return series


@router.patch('/series/{series_id}', response_model=SeriesRead, tags=['series'])
async def update_series(series_id: UUID, series_data: SeriesUpdate, db: AsyncSession = Depends(get_async_session)) -> SeriesRead:
    series = await SeriesService.update(db, series_id, series_data)
    if not series:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Series with id {series_id} not found')
    return series


@router.delete('/series/{series_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['series'])
async def delete_series(series_id: UUID, db: AsyncSession = Depends(get_async_session)) -> None:
    deleted = await SeriesService.delete(db, series_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Series with id {series_id} not found')

