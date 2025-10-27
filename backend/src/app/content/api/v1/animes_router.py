from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED

from app.content.schemas.content import AnimeCreate, AnimeRead, AnimeUpdate
from app.content.services.anime_service import AnimeService
from app.core.db import get_async_session

router = APIRouter(prefix='/content')


@router.post('/animes', response_model=AnimeRead, status_code=HTTP_201_CREATED, tags=['animes'])
async def create_anime(anime_data: AnimeCreate, db: AsyncSession = Depends(get_async_session)) -> AnimeRead:
    try:
        return await AnimeService.create(db, anime_data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.get('/animes', response_model=list[AnimeRead], tags=['animes'])
async def get_all_animes(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_session)) -> list[AnimeRead]:
    return await AnimeService.get_all(db, skip=skip, limit=limit)


@router.get('/animes/{anime_id}', response_model=AnimeRead, tags=['animes'])
async def get_anime(anime_id: UUID, db: AsyncSession = Depends(get_async_session)) -> AnimeRead:
    anime = await AnimeService.get_by_id(db, anime_id)
    if not anime:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Anime with id {anime_id} not found')
    return anime


@router.patch('/animes/{anime_id}', response_model=AnimeRead, tags=['animes'])
async def update_anime(anime_id: UUID, anime_data: AnimeUpdate, db: AsyncSession = Depends(get_async_session)) -> AnimeRead:
    anime = await AnimeService.update(db, anime_id, anime_data)
    if not anime:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Anime with id {anime_id} not found')
    return anime


@router.delete('/animes/{anime_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['animes'])
async def delete_anime(anime_id: UUID, db: AsyncSession = Depends(get_async_session)) -> None:
    deleted = await AnimeService.delete(db, anime_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Anime with id {anime_id} not found')

