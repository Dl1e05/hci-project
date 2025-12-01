from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_400_BAD_REQUEST

from app.core.db import get_async_session
from app.content.models.base import BaseContent
from app.references.models import DifficultyLevel


router = APIRouter(prefix='/content', tags=['recommendations'])



@router.get('/recommendations')
async def get_recommendations(
    limit: int = Query(10, ge=1, le=50, description='Number of content items to return'),
    language_level: Literal['A1', 'A2', 'B1', 'B2', 'C1', 'C2'] | None = Query(
        None,
        description='User language level (A1–C2). If provided, content difficulty will be <= this level.',
    ),
    db: AsyncSession = Depends(get_async_session),
):
    """
    Return latest content items of **any type**.

    If `language_level` is provided, only content with difficulty level **less than or equal**
    to the user level will be returned.
    """

    # Base query: any content type, only active, ordered by creation date
    base_query = select(BaseContent).where(BaseContent.is_active.is_(True))

    # Apply difficulty filter: difficulty_level.level <= user_level
    if language_level is not None:
        # 1) Find numeric difficulty level for the provided CEFR name (A1..C2)
        level_result = await db.execute(
            select(DifficultyLevel.level).where(DifficultyLevel.name == language_level)
        )
        user_level = level_result.scalar_one_or_none()

        if user_level is None:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=f'Unknown language level: {language_level}',
            )

        # 2) Join difficulty levels and filter by numeric level
        base_query = (
            base_query.join(BaseContent.difficulty_level)
            .where(DifficultyLevel.level <= user_level)
        )

    query = (
        base_query.order_by(BaseContent.created_at.desc())
        .limit(limit)
    )

    result = await db.execute(query)
    contents = list(result.scalars().all())

    return {
        'total': len(contents),
        'language_level': language_level,
        'items': contents,
    }