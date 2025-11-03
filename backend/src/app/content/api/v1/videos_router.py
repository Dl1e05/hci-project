from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED

from app.content.schemas.content import VideoCreate, VideoRead, VideoUpdate
from app.content.services.video_service import VideoService
from app.core.db import get_async_session

router = APIRouter(prefix='/content')


@router.post('/videos', response_model=VideoRead, status_code=HTTP_201_CREATED, tags=['videos'])
async def create_video(video_data: VideoCreate, db: AsyncSession = Depends(get_async_session)) -> VideoRead:
    try:
        return await VideoService.create(db, video_data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.get('/videos', response_model=list[VideoRead], tags=['videos'])
async def get_all_videos(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_session)) -> list[VideoRead]:
    return await VideoService.get_all(db, skip=skip, limit=limit)


@router.get('/videos/{video_id}', response_model=VideoRead, tags=['videos'])
async def get_video(video_id: UUID, db: AsyncSession = Depends(get_async_session)) -> VideoRead:
    video = await VideoService.get_by_id(db, video_id)
    if not video:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Video with id {video_id} not found')
    return video


@router.patch('/videos/{video_id}', response_model=VideoRead, tags=['videos'])
async def update_video(video_id: UUID, video_data: VideoUpdate, db: AsyncSession = Depends(get_async_session)) -> VideoRead:
    video = await VideoService.update(db, video_id, video_data)
    if not video:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Video with id {video_id} not found')
    return video


@router.delete('/videos/{video_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['videos'])
async def delete_video(video_id: UUID, db: AsyncSession = Depends(get_async_session)) -> None:
    deleted = await VideoService.delete(db, video_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Video with id {video_id} not found')

