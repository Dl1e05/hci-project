from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.reviews.schemas import ReviewCreate, ReviewRead, ReviewUpdate
from app.reviews.service import ReviewService

router = APIRouter(prefix='/reviews', tags=['reviews'])


@router.post('', response_model=ReviewRead, status_code=status.HTTP_201_CREATED)
async def create_review(
    review_data: ReviewCreate,
    db: AsyncSession = Depends(get_async_session),
) -> ReviewRead:
    """Create a new review"""
    try:
        return await ReviewService.create(db, review_data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.get('', response_model=list[ReviewRead])
async def get_reviews(
    content_id: UUID | None = Query(None, description='Filter by content ID'),
    user_id: UUID | None = Query(None, description='Filter by user ID'),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_async_session),
) -> list[ReviewRead]:
    """Get reviews filtered by content_id or user_id"""
    if content_id:
        return await ReviewService.get_by_content_id(db, content_id, skip, limit)
    if user_id:
        return await ReviewService.get_by_user_id(db, user_id, skip, limit)
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Either content_id or user_id must be provided',
    )


@router.get('/{review_id}', response_model=ReviewRead)
async def get_review(
    review_id: UUID,
    db: AsyncSession = Depends(get_async_session),
) -> ReviewRead:
    """Get a specific review by ID"""
    review = await ReviewService.get_by_id(db, review_id)
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Review with id {review_id} not found')
    return review


@router.patch('/{review_id}', response_model=ReviewRead)
async def update_review(
    review_id: UUID,
    review_data: ReviewUpdate,
    db: AsyncSession = Depends(get_async_session),
) -> ReviewRead:
    """Update a review (partial update)"""
    review = await ReviewService.update(db, review_id, review_data)
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Review with id {review_id} not found')
    return review


@router.delete('/{review_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(
    review_id: UUID,
    db: AsyncSession = Depends(get_async_session),
) -> None:
    """Delete a review"""
    deleted = await ReviewService.delete(db, review_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Review with id {review_id} not found')
