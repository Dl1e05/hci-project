from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED

from app.references.schemas import PlatformCreate, PlatformRead, PlatformUpdate
from app.references.services.platform_service import PlatformService
from app.core.db import get_async_session

router = APIRouter(prefix='/content')


@router.post('/platforms', response_model=PlatformRead, status_code=HTTP_201_CREATED, tags=['platforms'])
async def create_platform(platform_data: PlatformCreate, db: AsyncSession = Depends(get_async_session)) -> PlatformRead:
    existing_platform = await PlatformService.get_by_name(db, platform_data.name)
    if existing_platform:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Platform with name '{platform_data.name}' already exists"
        )
    return await PlatformService.create(db, platform_data)


@router.get('/platforms', response_model=list[PlatformRead], tags=['platforms'])
async def get_all_platforms(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_session)) -> list[PlatformRead]:
    return await PlatformService.get_all(db, skip=skip, limit=limit)


@router.get('/platforms/{platform_id}', response_model=PlatformRead, tags=['platforms'])
async def get_platform(platform_id: int, db: AsyncSession = Depends(get_async_session)) -> PlatformRead:
    platform = await PlatformService.get_by_id(db, platform_id)
    if not platform:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Platform with id {platform_id} not found')
    return platform


@router.patch('/platforms/{platform_id}', response_model=PlatformRead, tags=['platforms'])
async def update_platform(platform_id: int, platform_data: PlatformUpdate, db: AsyncSession = Depends(get_async_session)) -> PlatformRead:
    if platform_data.name:
        existing_platform = await PlatformService.get_by_name(db, platform_data.name)
        if existing_platform and existing_platform.id != platform_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Platform with name '{platform_data.name}' already exists"
            )

    platform = await PlatformService.update(db, platform_id, platform_data)
    if not platform:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Platform with id {platform_id} not found')
    return platform


@router.delete('/platforms/{platform_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['platforms'])
async def delete_platform(platform_id: int, db: AsyncSession = Depends(get_async_session)) -> None:
    deleted = await PlatformService.delete(db, platform_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Platform with id {platform_id} not found')

