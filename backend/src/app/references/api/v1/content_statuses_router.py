from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED

from app.references.schemas import ContentStatusCreate, ContentStatusRead, ContentStatusUpdate
from app.references.services.content_status_service import ContentStatusService
from app.core.db import get_async_session

router = APIRouter(prefix='/content')


@router.post('/content-statuses', response_model=ContentStatusRead, status_code=HTTP_201_CREATED, tags=['content-statuses'])
async def create_content_status(status_data: ContentStatusCreate, db: AsyncSession = Depends(get_async_session)) -> ContentStatusRead:
    existing_status = await ContentStatusService.get_by_name(db, status_data.name)
    if existing_status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Content status with name '{status_data.name}' already exists"
        )
    return await ContentStatusService.create(db, status_data)


@router.get('/content-statuses', response_model=list[ContentStatusRead], tags=['content-statuses'])
async def get_all_content_statuses(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_session)) -> list[ContentStatusRead]:
    return await ContentStatusService.get_all(db, skip=skip, limit=limit)


@router.get('/content-statuses/{status_id}', response_model=ContentStatusRead, tags=['content-statuses'])
async def get_content_status(status_id: int, db: AsyncSession = Depends(get_async_session)) -> ContentStatusRead:
    content_status = await ContentStatusService.get_by_id(db, status_id)
    if not content_status:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Content status with id {status_id} not found')
    return content_status


@router.patch('/content-statuses/{status_id}', response_model=ContentStatusRead, tags=['content-statuses'])
async def update_content_status(status_id: int, status_data: ContentStatusUpdate, db: AsyncSession = Depends(get_async_session)) -> ContentStatusRead:
    if status_data.name:
        existing_status = await ContentStatusService.get_by_name(db, status_data.name)
        if existing_status and existing_status.id != status_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Content status with name '{status_data.name}' already exists"
            )

    content_status = await ContentStatusService.update(db, status_id, status_data)
    if not content_status:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Content status with id {status_id} not found')
    return content_status


@router.delete('/content-statuses/{status_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['content-statuses'])
async def delete_content_status(status_id: int, db: AsyncSession = Depends(get_async_session)) -> None:
    deleted = await ContentStatusService.delete(db, status_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Content status with id {status_id} not found')

