from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED

from app.content.schemas import (
    ContentTypeCreate,
    ContentTypeRead,
    ContentTypeUpdate,
    TagsCreate,
    TagsRead,
    TagsUpdate,
)
from app.content.services.content_types import ContentTypesService
from app.content.services.tags import TagsService
from app.core.db import get_async_session

router = APIRouter(
    prefix="/content",
    tags=["content"]
)

@router.post("/tags", response_model=TagsRead, status_code=HTTP_201_CREATED, tags=["tags"])
async def create_tag(tag_data: TagsCreate, db: AsyncSession = Depends(get_async_session)) -> TagsRead:
    existing_tag = await TagsService.get_by_code(db, tag_data.code)
    if existing_tag:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Tag with code '{tag_data.code}' already exists")
    
    return await TagsService.create(db, tag_data)

@router.get("/tags", response_model=list[TagsRead], tags=["tags"])
async def get_all_tags(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_session)) -> list[TagsRead]:
    return await TagsService.get_all(db, skip=skip, limit=limit)

@router.get("/tags/{tag_id}", response_model=TagsRead, tags=["tags"])
async def get_tag(tag_id: UUID, db: AsyncSession = Depends(get_async_session)) -> TagsRead:
    tag = await TagsService.get_by_id(db, tag_id)
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Tag with id {tag_id} not found")
    
    return tag

@router.patch("/tags/{tag_id}", response_model=TagsRead, tags=["Tags"])
async def update_tag(tag_id: UUID, tag_data: TagsUpdate, db: AsyncSession = Depends(get_async_session)) -> TagsRead:
    if tag_data.code:
        existing_tag = await TagsService.get_by_code(db, tag_data.code)
        if existing_tag and existing_tag.id != tag_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Tag with code '{tag_data.code}' already exists"
            )
        
    tag = await TagsService.update(db, tag_id, tag_data)
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Tag with id {tag_id} not found")
    
    return tag

@router.delete("/tags/{tag_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Tags"])
async def delete_tag(tag_id: UUID, db: AsyncSession = Depends(get_async_session)) -> None:
    deleted = await TagsService.delete(db, tag_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Tag with id {tag_id} not found")
    
# ========================================================================== #

@router.post("/content-types", response_model=ContentTypeRead, status_code=HTTP_201_CREATED, tags=["content-types"])
async def create_content_type(
        content_type_data: ContentTypeCreate, 
        db: AsyncSession = Depends(get_async_session)
    ) -> ContentTypeRead:

    return await ContentTypesService.create(db, content_type_data)

@router.get("/content-types", response_model=list[ContentTypeRead], tags=["content-types"])
async def get_content_types(
        skip: int = 0, 
        limit: int = 100, 
        db: AsyncSession = Depends(get_async_session)
    ) -> list[ContentTypeRead]:

    return await ContentTypesService.get_all(db, skip=skip, limit=limit)

@router.get("/content-types/{content_type_id}", response_model=ContentTypeRead, tags=["content-types"])
async def get_content_type(content_type_id: UUID, db: AsyncSession = Depends(get_async_session)) -> ContentTypeRead:
    content_type = await ContentTypesService.get_by_id(db, content_type_id)
    if not content_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Content type with id {content_type_id} not found")
    
    return content_type

@router.patch("/content-types/{content_type_id}", response_model=ContentTypeRead, tags=["content-types"])
async def update_content_type(
    content_type_id: UUID, 
    content_type_data: ContentTypeUpdate, 
    db: AsyncSession = Depends(get_async_session)
    ) -> ContentTypeRead:

    content_type = await ContentTypesService.update(db, content_type_id, content_type_data)
    if not content_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Content type with id {content_type_id} not found")
    
    return content_type

@router.delete("/content-types/{content_type_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["content-types"])
async def delete_content_type(content_type_id: UUID, db: AsyncSession = Depends(get_async_session)) -> None:
    deleted = await ContentTypesService.delete(db, content_type_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Content type with id {content_type_id} not found")