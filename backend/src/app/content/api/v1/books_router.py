from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED

from app.content.schemas.content import BookRead, BookUpdate
from app.content.schemas.filters import BookFilterParams
from app.content.schemas.forms import BookFormData
from app.content.schemas.pagination import PaginatedResponse, PaginationParams
from app.content.services.book_service import BookService
from app.core.db import get_async_session
from app.core.storage import get_storage_service

router = APIRouter(prefix='/content')


@router.post('/books', response_model=BookRead, status_code=HTTP_201_CREATED, tags=['books'])
async def create_book(
    form_data: BookFormData = Depends(),
    banner: UploadFile = File(...),
    db: AsyncSession = Depends(get_async_session),
) -> BookRead:
    try:
        storage = get_storage_service()
        banner_key = storage.upload_file(banner.file, banner.filename or 'banner', banner.content_type, 'banners')
        banner_url = storage.get_public_url(banner_key)
        book_data = form_data.to_schema(banner_url=banner_url)
        return await BookService.create(db, book_data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.get('/books/search', response_model=PaginatedResponse[BookRead], tags=['books'])
async def search_books(
    filters: BookFilterParams = Depends(),
    pagination: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_async_session),
) -> PaginatedResponse[BookRead]:
    """Search and filter books with pagination"""
    books, total = await BookService.get_filtered(db, filters, skip=pagination.skip, limit=pagination.limit)
    return PaginatedResponse.create(items=books, total=total, skip=pagination.skip, limit=pagination.limit)


@router.get('/books', response_model=list[BookRead], tags=['books'])
async def get_all_books(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_session)) -> list[BookRead]:
    return await BookService.get_all(db, skip=skip, limit=limit)


@router.get('/books/{book_id}', response_model=BookRead, tags=['books'])
async def get_book(book_id: UUID, db: AsyncSession = Depends(get_async_session)) -> BookRead:
    book = await BookService.get_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Book with id {book_id} not found')
    return book


@router.patch('/books/{book_id}', response_model=BookRead, tags=['books'])
async def update_book(book_id: UUID, book_data: BookUpdate, db: AsyncSession = Depends(get_async_session)) -> BookRead:
    book = await BookService.update(db, book_id, book_data)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Book with id {book_id} not found')
    return book


@router.delete('/books/{book_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['books'])
async def delete_book(book_id: UUID, db: AsyncSession = Depends(get_async_session)) -> None:
    deleted = await BookService.delete(db, book_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Book with id {book_id} not found')
