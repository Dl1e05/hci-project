from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED

from app.references.schemas import ContentCategoryCreate, ContentCategoryRead, ContentCategoryUpdate
from app.references.services.content_category_service import ContentCategoryService
from app.core.db import get_async_session

router = APIRouter(prefix='/content')


@router.post('/content-categories', response_model=ContentCategoryRead, status_code=HTTP_201_CREATED, tags=['content-categories'])
async def create_content_category(category_data: ContentCategoryCreate, db: AsyncSession = Depends(get_async_session)) -> ContentCategoryRead:
    existing_category = await ContentCategoryService.get_by_name(db, category_data.name)
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Content category with name '{category_data.name}' already exists"
        )
    return await ContentCategoryService.create(db, category_data)


@router.get('/content-categories', response_model=list[ContentCategoryRead], tags=['content-categories'])
async def get_all_content_categories(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_session)) -> list[ContentCategoryRead]:
    return await ContentCategoryService.get_all(db, skip=skip, limit=limit)


@router.get('/content-categories/{category_id}', response_model=ContentCategoryRead, tags=['content-categories'])
async def get_content_category(category_id: UUID, db: AsyncSession = Depends(get_async_session)) -> ContentCategoryRead:
    category = await ContentCategoryService.get_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Content category with id {category_id} not found')
    return category


@router.patch('/content-categories/{category_id}', response_model=ContentCategoryRead, tags=['content-categories'])
async def update_content_category(category_id: UUID, category_data: ContentCategoryUpdate, db: AsyncSession = Depends(get_async_session)) -> ContentCategoryRead:
    if category_data.name:
        existing_category = await ContentCategoryService.get_by_name(db, category_data.name)
        if existing_category and existing_category.id != category_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Content category with name '{category_data.name}' already exists"
            )

    category = await ContentCategoryService.update(db, category_id, category_data)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Content category with id {category_id} not found')
    return category


@router.delete('/content-categories/{category_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['content-categories'])
async def delete_content_category(category_id: UUID, db: AsyncSession = Depends(get_async_session)) -> None:
    deleted = await ContentCategoryService.delete(db, category_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Content category with id {category_id} not found')

