from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED

from app.references.schemas import AuthorCreate, AuthorRead, AuthorUpdate
from app.references.services.author_service import AuthorService
from app.core.db import get_async_session

router = APIRouter(prefix='/content')


@router.post('/authors', response_model=AuthorRead, status_code=HTTP_201_CREATED, tags=['authors'])
async def create_author(author_data: AuthorCreate, db: AsyncSession = Depends(get_async_session)) -> AuthorRead:
    existing_author = await AuthorService.get_by_name(db, author_data.full_name)
    if existing_author:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Author with name '{author_data.full_name}' already exists"
        )
    return await AuthorService.create(db, author_data)


@router.get('/authors', response_model=list[AuthorRead], tags=['authors'])
async def get_all_authors(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_session)) -> list[AuthorRead]:
    return await AuthorService.get_all(db, skip=skip, limit=limit)


@router.get('/authors/{author_id}', response_model=AuthorRead, tags=['authors'])
async def get_author(author_id: int, db: AsyncSession = Depends(get_async_session)) -> AuthorRead:
    author = await AuthorService.get_by_id(db, author_id)
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Author with id {author_id} not found')
    return author


@router.patch('/authors/{author_id}', response_model=AuthorRead, tags=['authors'])
async def update_author(author_id: int, author_data: AuthorUpdate, db: AsyncSession = Depends(get_async_session)) -> AuthorRead:
    if author_data.full_name:
        existing_author = await AuthorService.get_by_name(db, author_data.full_name)
        if existing_author and existing_author.id != author_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Author with name '{author_data.full_name}' already exists"
            )

    author = await AuthorService.update(db, author_id, author_data)
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Author with id {author_id} not found')
    return author


@router.delete('/authors/{author_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['authors'])
async def delete_author(author_id: int, db: AsyncSession = Depends(get_async_session)) -> None:
    deleted = await AuthorService.delete(db, author_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Author with id {author_id} not found')

