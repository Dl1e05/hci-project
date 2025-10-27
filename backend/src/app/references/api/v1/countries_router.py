from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED

from app.references.schemas import CountryCreate, CountryRead, CountryUpdate
from app.references.services.country_service import CountryService
from app.core.db import get_async_session

router = APIRouter(prefix='/content')


@router.post('/countries', response_model=CountryRead, status_code=HTTP_201_CREATED, tags=['countries'])
async def create_country(country_data: CountryCreate, db: AsyncSession = Depends(get_async_session)) -> CountryRead:
    existing_country = await CountryService.get_by_code(db, country_data.code)
    if existing_country:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Country with code '{country_data.code}' already exists"
        )
    return await CountryService.create(db, country_data)


@router.get('/countries', response_model=list[CountryRead], tags=['countries'])
async def get_all_countries(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_session)) -> list[CountryRead]:
    return await CountryService.get_all(db, skip=skip, limit=limit)


@router.get('/countries/{country_id}', response_model=CountryRead, tags=['countries'])
async def get_country(country_id: UUID, db: AsyncSession = Depends(get_async_session)) -> CountryRead:
    country = await CountryService.get_by_id(db, country_id)
    if not country:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Country with id {country_id} not found')
    return country


@router.patch('/countries/{country_id}', response_model=CountryRead, tags=['countries'])
async def update_country(country_id: UUID, country_data: CountryUpdate, db: AsyncSession = Depends(get_async_session)) -> CountryRead:
    if country_data.code:
        existing_country = await CountryService.get_by_code(db, country_data.code)
        if existing_country and existing_country.id != country_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Country with code '{country_data.code}' already exists"
            )

    country = await CountryService.update(db, country_id, country_data)
    if not country:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Country with id {country_id} not found')
    return country


@router.delete('/countries/{country_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['countries'])
async def delete_country(country_id: UUID, db: AsyncSession = Depends(get_async_session)) -> None:
    deleted = await CountryService.delete(db, country_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Country with id {country_id} not found')

