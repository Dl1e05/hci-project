from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.content.models.content import Book
from app.content.repo import ContentRepository
from app.content.schemas.content import BookCreate, BookRead, BookUpdate


class BookService:
    @staticmethod
    async def create(db: AsyncSession, book_data: BookCreate) -> BookRead:
        data = book_data.model_dump()
        book = await ContentRepository.create(db, Book, data)
        return BookRead.model_validate(book)

    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[BookRead]:
        books = await ContentRepository.get_all(db, Book, skip, limit)
        return [BookRead.model_validate(book) for book in books]

    @staticmethod
    async def get_by_id(db: AsyncSession, book_id: UUID) -> BookRead | None:
        book = await ContentRepository.get_by_id(db, Book, book_id)
        return BookRead.model_validate(book) if book else None

    @staticmethod
    async def update(db: AsyncSession, book_id: UUID, book_data: BookUpdate) -> BookRead | None:
        data = book_data.model_dump(exclude_unset=True)
        book = await ContentRepository.update(db, Book, book_id, data)
        return BookRead.model_validate(book) if book else None

    @staticmethod
    async def delete(db: AsyncSession, book_id: UUID) -> bool:
        return await ContentRepository.delete(db, Book, book_id)

