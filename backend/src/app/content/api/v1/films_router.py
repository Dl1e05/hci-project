from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED

from app.content.schemas.content import FilmCreate, FilmRead, FilmUpdate
from app.content.services.film_service import FilmService
from app.core.db import get_async_session

router = APIRouter(prefix='/content')


@router.post('/films', response_model=FilmRead, status_code=HTTP_201_CREATED, tags=['films'])
async def create_film(film_data: FilmCreate, db: AsyncSession = Depends(get_async_session)) -> FilmRead:
    try:
        return await FilmService.create(db, film_data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.get('/films', response_model=list[FilmRead], tags=['films'])
async def get_all_films(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_session)) -> list[FilmRead]:
    return await FilmService.get_all(db, skip=skip, limit=limit)


@router.get('/films/{film_id}', response_model=FilmRead, tags=['films'])
async def get_film(film_id: UUID, db: AsyncSession = Depends(get_async_session)) -> FilmRead:
    film = await FilmService.get_by_id(db, film_id)
    if not film:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Film with id {film_id} not found')
    return film


@router.patch('/films/{film_id}', response_model=FilmRead, tags=['films'])
async def update_film(film_id: UUID, film_data: FilmUpdate, db: AsyncSession = Depends(get_async_session)) -> FilmRead:
    film = await FilmService.update(db, film_id, film_data)
    if not film:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Film with id {film_id} not found')
    return film


@router.delete('/films/{film_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['films'])
async def delete_film(film_id: UUID, db: AsyncSession = Depends(get_async_session)) -> None:
    deleted = await FilmService.delete(db, film_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Film with id {film_id} not found')

