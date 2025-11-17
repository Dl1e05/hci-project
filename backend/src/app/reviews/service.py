from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.reviews.models import Review
from app.reviews.schemas import ReviewCreate, ReviewRead, ReviewUpdate


class ReviewService:
    @staticmethod
    async def create(db: AsyncSession, review_data: ReviewCreate) -> ReviewRead:
        """Create a new review"""
        data = review_data.model_dump(mode='python')
        review = Review(**data)
        db.add(review)
        await db.commit()
        await db.refresh(review)
        return ReviewRead.model_validate(review)

    @staticmethod
    async def get_by_id(db: AsyncSession, review_id: UUID) -> ReviewRead | None:
        """Get a review by ID"""
        result = await db.execute(select(Review).where(Review.id == review_id))
        review = result.scalar_one_or_none()
        return ReviewRead.model_validate(review) if review else None

    @staticmethod
    async def get_by_content_id(db: AsyncSession, content_id: UUID, skip: int = 0, limit: int = 100) -> list[ReviewRead]:
        """Get all reviews for a specific content"""
        result = await db.execute(select(Review).where(Review.content_id == content_id).offset(skip).limit(limit))
        reviews = result.scalars().all()
        return [ReviewRead.model_validate(review) for review in reviews]

    @staticmethod
    async def get_by_user_id(db: AsyncSession, user_id: UUID, skip: int = 0, limit: int = 100) -> list[ReviewRead]:
        """Get all reviews by a specific user"""
        result = await db.execute(select(Review).where(Review.user_id == user_id).offset(skip).limit(limit))
        reviews = result.scalars().all()
        return [ReviewRead.model_validate(review) for review in reviews]

    @staticmethod
    async def update(db: AsyncSession, review_id: UUID, review_data: ReviewUpdate) -> ReviewRead | None:
        """Update a review"""
        result = await db.execute(select(Review).where(Review.id == review_id))
        review = result.scalar_one_or_none()

        if not review:
            return None

        update_data = review_data.model_dump(exclude_unset=True, mode='python')
        for field, value in update_data.items():
            if hasattr(review, field):
                setattr(review, field, value)

        await db.commit()
        await db.refresh(review)
        return ReviewRead.model_validate(review)

    @staticmethod
    async def delete(db: AsyncSession, review_id: UUID) -> bool:
        """Delete a review"""
        result = await db.execute(delete(Review).where(Review.id == review_id))
        await db.commit()
        return result.rowcount > 0
