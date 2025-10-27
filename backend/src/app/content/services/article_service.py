from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.content.models.content import Article
from app.content.repo import ContentRepository
from app.content.schemas.content import ArticleCreate, ArticleRead, ArticleUpdate


class ArticleService:
    @staticmethod
    async def create(db: AsyncSession, article_data: ArticleCreate) -> ArticleRead:
        data = article_data.model_dump()
        article = await ContentRepository.create(db, Article, data)
        return ArticleRead.model_validate(article)

    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[ArticleRead]:
        articles = await ContentRepository.get_all(db, Article, skip, limit)
        return [ArticleRead.model_validate(article) for article in articles]

    @staticmethod
    async def get_by_id(db: AsyncSession, article_id: UUID) -> ArticleRead | None:
        article = await ContentRepository.get_by_id(db, Article, article_id)
        return ArticleRead.model_validate(article) if article else None

    @staticmethod
    async def update(db: AsyncSession, article_id: UUID, article_data: ArticleUpdate) -> ArticleRead | None:
        data = article_data.model_dump(exclude_unset=True)
        article = await ContentRepository.update(db, Article, article_id, data)
        return ArticleRead.model_validate(article) if article else None

    @staticmethod
    async def delete(db: AsyncSession, article_id: UUID) -> bool:
        return await ContentRepository.delete(db, Article, article_id)

