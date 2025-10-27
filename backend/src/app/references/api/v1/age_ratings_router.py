from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED

from app.references.schemas import AgeRatingCreate, AgeRatingRead, AgeRatingUpdate
from app.references.services.age_rating_service import AgeRatingService
from app.core.db import get_async_session

router = APIRouter(prefix='/content')


@router.post('/age-ratings', response_model=AgeRatingRead, status_code=HTTP_201_CREATED, tags=['age-ratings'])
async def create_age_rating(age_rating_data: AgeRatingCreate, db: AsyncSession = Depends(get_async_session)) -> AgeRatingRead:
    existing_age_rating = await AgeRatingService.get_by_value(db, age_rating_data.value)
    if existing_age_rating:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Age rating with value '{age_rating_data.value}' already exists"
        )
    return await AgeRatingService.create(db, age_rating_data)


@router.get('/age-ratings', response_model=list[AgeRatingRead], tags=['age-ratings'])
async def get_all_age_ratings(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_session)) -> list[AgeRatingRead]:
    return await AgeRatingService.get_all(db, skip=skip, limit=limit)


@router.get('/age-ratings/{age_rating_id}', response_model=AgeRatingRead, tags=['age-ratings'])
async def get_age_rating(age_rating_id: int, db: AsyncSession = Depends(get_async_session)) -> AgeRatingRead:
    age_rating = await AgeRatingService.get_by_id(db, age_rating_id)
    if not age_rating:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Age rating with id {age_rating_id} not found')
    return age_rating


@router.patch('/age-ratings/{age_rating_id}', response_model=AgeRatingRead, tags=['age-ratings'])
async def update_age_rating(age_rating_id: int, age_rating_data: AgeRatingUpdate, db: AsyncSession = Depends(get_async_session)) -> AgeRatingRead:
    if age_rating_data.value:
        existing_age_rating = await AgeRatingService.get_by_value(db, age_rating_data.value)
        if existing_age_rating and existing_age_rating.id != age_rating_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Age rating with value '{age_rating_data.value}' already exists"
            )

    age_rating = await AgeRatingService.update(db, age_rating_id, age_rating_data)
    if not age_rating:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Age rating with id {age_rating_id} not found')
    return age_rating


@router.delete('/age-ratings/{age_rating_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['age-ratings'])
async def delete_age_rating(age_rating_id: int, db: AsyncSession = Depends(get_async_session)) -> None:
    deleted = await AgeRatingService.delete(db, age_rating_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Age rating with id {age_rating_id} not found')

