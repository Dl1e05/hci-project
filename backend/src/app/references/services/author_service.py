from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.references.models import Author
from app.references.schemas import AuthorCreate, AuthorRead, AuthorUpdate


class AuthorService:
    @staticmethod
    async def create(db: AsyncSession, author_data: AuthorCreate) -> AuthorRead:
        author = Author(**author_data.model_dump())
        db.add(author)
        await db.commit()
        await db.refresh(author)
        return AuthorRead.model_validate(author)

    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[AuthorRead]:
        result = await db.execute(select(Author).offset(skip).limit(limit).order_by(Author.full_name))
        authors = result.scalars().all()
        return [AuthorRead.model_validate(author) for author in authors]

    @staticmethod
    async def get_by_id(db: AsyncSession, author_id: int) -> AuthorRead | None:
        result = await db.execute(select(Author).where(Author.id == author_id))
        author = result.scalar_one_or_none()
        return AuthorRead.model_validate(author) if author else None

    @staticmethod
    async def get_by_name(db: AsyncSession, full_name: str) -> Author | None:
        result = await db.execute(select(Author).where(Author.full_name == full_name))
        return result.scalar_one_or_none()

    @staticmethod
    async def update(db: AsyncSession, author_id: int, author_data: AuthorUpdate) -> AuthorRead | None:
        result = await db.execute(select(Author).where(Author.id == author_id))
        author_entity = result.scalar_one_or_none()
        if not author_entity:
            return None

        update_data = author_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(author_entity, field, value)

        await db.commit()
        await db.refresh(author_entity)
        return AuthorRead.model_validate(author_entity)

    @staticmethod
    async def delete(db: AsyncSession, author_id: int) -> bool:
        result = await db.execute(select(Author).where(Author.id == author_id))
        author_entity = result.scalar_one_or_none()
        if not author_entity:
            return False

        await db.delete(author_entity)
        await db.commit()
        return True

