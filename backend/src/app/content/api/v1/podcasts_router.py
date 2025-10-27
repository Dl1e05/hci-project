from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED

from app.content.schemas.content import PodcastCreate, PodcastRead, PodcastUpdate
from app.content.services.podcast_service import PodcastService
from app.core.db import get_async_session

router = APIRouter(prefix='/content')


@router.post('/podcasts', response_model=PodcastRead, status_code=HTTP_201_CREATED, tags=['podcasts'])
async def create_podcast(podcast_data: PodcastCreate, db: AsyncSession = Depends(get_async_session)) -> PodcastRead:
    try:
        return await PodcastService.create(db, podcast_data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.get('/podcasts', response_model=list[PodcastRead], tags=['podcasts'])
async def get_all_podcasts(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_session)) -> list[PodcastRead]:
    return await PodcastService.get_all(db, skip=skip, limit=limit)


@router.get('/podcasts/{podcast_id}', response_model=PodcastRead, tags=['podcasts'])
async def get_podcast(podcast_id: UUID, db: AsyncSession = Depends(get_async_session)) -> PodcastRead:
    podcast = await PodcastService.get_by_id(db, podcast_id)
    if not podcast:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Podcast with id {podcast_id} not found')
    return podcast


@router.patch('/podcasts/{podcast_id}', response_model=PodcastRead, tags=['podcasts'])
async def update_podcast(podcast_id: UUID, podcast_data: PodcastUpdate, db: AsyncSession = Depends(get_async_session)) -> PodcastRead:
    podcast = await PodcastService.update(db, podcast_id, podcast_data)
    if not podcast:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Podcast with id {podcast_id} not found')
    return podcast


@router.delete('/podcasts/{podcast_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['podcasts'])
async def delete_podcast(podcast_id: UUID, db: AsyncSession = Depends(get_async_session)) -> None:
    deleted = await PodcastService.delete(db, podcast_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Podcast with id {podcast_id} not found')

