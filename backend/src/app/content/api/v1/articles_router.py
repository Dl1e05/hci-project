from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED

from app.content.schemas.content import ArticleCreate, ArticleRead, ArticleUpdate
from app.content.services.article_service import ArticleService
from app.core.db import get_async_session

router = APIRouter(prefix='/content')


@router.post('/articles', response_model=ArticleRead, status_code=HTTP_201_CREATED, tags=['articles'])
async def create_article(article_data: ArticleCreate, db: AsyncSession = Depends(get_async_session)) -> ArticleRead:
    try:
        return await ArticleService.create(db, article_data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.get('/articles', response_model=list[ArticleRead], tags=['articles'])
async def get_all_articles(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_session)) -> list[ArticleRead]:
    return await ArticleService.get_all(db, skip=skip, limit=limit)


@router.get('/articles/{article_id}', response_model=ArticleRead, tags=['articles'])
async def get_article(article_id: UUID, db: AsyncSession = Depends(get_async_session)) -> ArticleRead:
    article = await ArticleService.get_by_id(db, article_id)
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Article with id {article_id} not found')
    return article


@router.patch('/articles/{article_id}', response_model=ArticleRead, tags=['articles'])
async def update_article(article_id: UUID, article_data: ArticleUpdate, db: AsyncSession = Depends(get_async_session)) -> ArticleRead:
    article = await ArticleService.update(db, article_id, article_data)
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Article with id {article_id} not found')
    return article


@router.delete('/articles/{article_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['articles'])
async def delete_article(article_id: UUID, db: AsyncSession = Depends(get_async_session)) -> None:
    deleted = await ArticleService.delete(db, article_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Article with id {article_id} not found')

