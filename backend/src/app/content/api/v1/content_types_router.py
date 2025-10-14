import traceback
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED

from app.content.schemas import (
    ContentTypeCreate,
    ContentTypeRead,
    ContentTypeUpdate,
)
from app.content.services.content_types_service import ContentTypesService
from app.core.db import get_async_session

router = APIRouter(prefix='/content')


@router.post('/content-types', response_model=ContentTypeRead, status_code=HTTP_201_CREATED, tags=['content-types'])
async def create_content_type(
    content_type_data: ContentTypeCreate, db: AsyncSession = Depends(get_async_session)
) -> ContentTypeRead:
    try:
        return await ContentTypesService.create(db, content_type_data)
    except Exception as e:
        print(f'Error creating content type: {str(e)}')
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Internal server error: {str(e)}') from e


@router.get('/content-types', response_model=list[ContentTypeRead], tags=['content-types'])
async def get_content_types(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_session)
) -> list[ContentTypeRead]:
    return await ContentTypesService.get_all(db, skip=skip, limit=limit)


@router.get('/content-types/{content_type_id}', response_model=ContentTypeRead, tags=['content-types'])
async def get_content_type(content_type_id: UUID, db: AsyncSession = Depends(get_async_session)) -> ContentTypeRead:
    content_type = await ContentTypesService.get_by_id(db, content_type_id)
    if not content_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Content type with id {content_type_id} not found')

    return content_type


@router.patch('/content-types/{content_type_id}', response_model=ContentTypeRead, tags=['content-types'])
async def update_content_type(
    content_type_id: UUID, content_type_data: ContentTypeUpdate, db: AsyncSession = Depends(get_async_session)
) -> ContentTypeRead:
    content_type = await ContentTypesService.update(db, content_type_id, content_type_data)
    if not content_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Content type with id {content_type_id} not found')

    return content_type


@router.delete('/content-types/{content_type_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['content-types'])
async def delete_content_type(content_type_id: UUID, db: AsyncSession = Depends(get_async_session)) -> None:
    deleted = await ContentTypesService.delete(db, content_type_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Content type with id {content_type_id} not found')
