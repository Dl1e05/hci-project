from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED

from app.references.schemas import GenresCreate, GenresRead, GenresUpdate
from app.references.services.genres_service import GenresService
from app.core.db import get_async_session

router = APIRouter(prefix='/content')


@router.post('/genres', response_model=GenresRead, status_code=HTTP_201_CREATED, tags=['genres'])
async def create_genre(genre_data: GenresCreate, db: AsyncSession = Depends(get_async_session)) -> GenresRead:
    existing_genre = await GenresService.get_by_name(db, genre_data.name)
    if existing_genre:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Genre with name '{genre_data.name}' already exists"
        )
    return await GenresService.create(db, genre_data)


@router.get('/genres', response_model=list[GenresRead], tags=['genres'])
async def get_all_genres(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_session)) -> list[GenresRead]:
    return await GenresService.get_all(db, skip=skip, limit=limit)


@router.get('/genres/{genre_id}', response_model=GenresRead, tags=['genres'])
async def get_genre(genre_id: UUID, db: AsyncSession = Depends(get_async_session)) -> GenresRead:
    genre = await GenresService.get_by_id(db, genre_id)
    if not genre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Genre with id {genre_id} not found')
    return genre


@router.patch('/genres/{genre_id}', response_model=GenresRead, tags=['genres'])
async def update_genre(genre_id: UUID, genre_data: GenresUpdate, db: AsyncSession = Depends(get_async_session)) -> GenresRead:
    if genre_data.name:
        existing_genre = await GenresService.get_by_name(db, genre_data.name)
        if existing_genre and existing_genre.id != genre_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Genre with name '{genre_data.name}' already exists"
            )

    genre = await GenresService.update(db, genre_id, genre_data)
    if not genre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Genre with id {genre_id} not found')
    return genre


@router.delete('/genres/{genre_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['genres'])
async def delete_genre(genre_id: UUID, db: AsyncSession = Depends(get_async_session)) -> None:
    deleted = await GenresService.delete(db, genre_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Genre with id {genre_id} not found')

