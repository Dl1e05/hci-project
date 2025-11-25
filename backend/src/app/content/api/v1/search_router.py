from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.content.schemas.search import ContentSearchParams, ContentSearchResult
from app.content.services.search_service import SearchService
from app.core.db import get_async_session

router = APIRouter(prefix='/content')


@router.get('/search', response_model=ContentSearchResult, tags=['search'])
async def search_content(
    search: str | None = Query(None, min_length=1, max_length=200),
    title: str | None = Query(None, min_length=1, max_length=128),
    short_description: str | None = Query(None, min_length=1, max_length=500),
    long_description: str | None = Query(None, min_length=1, max_length=10000),
    keywords: str | None = Query(None, min_length=1, max_length=500),
    content_types: list[str] | None = Query(None),
    genre_ids: list[str] | None = Query(None),
    tag_ids: list[str] | None = Query(None),
    audio_language_ids: list[int] | None = Query(None),
    subtitle_language_ids: list[int] | None = Query(None),
    original_language_id: int | None = Query(None),
    age_rating_id: int | None = Query(None),
    author_id: int | None = Query(None),
    country_id: str | None = Query(None),
    difficulty_level_id: int | None = Query(None),
    min_rating: float | None = Query(None, ge=0, le=10),
    max_rating: float | None = Query(None, ge=0, le=10),
    release_date_from: str | None = Query(None),
    release_date_to: str | None = Query(None),
    is_active: bool | None = Query(None),
    sort_by: str | None = Query('created_at'),
    sort_order: str = Query('desc'),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_async_session),
) -> ContentSearchResult:
    params = ContentSearchParams(
        search=search,
        title=title,
        short_description=short_description,
        long_description=long_description,
        keywords=keywords,
        content_types=content_types,
        genre_ids=genre_ids,
        tag_ids=tag_ids,
        audio_language_ids=audio_language_ids,
        subtitle_language_ids=subtitle_language_ids,
        original_language_id=original_language_id,
        age_rating_id=age_rating_id,
        author_id=author_id,
        country_id=country_id,
        difficulty_level_id=difficulty_level_id,
        min_rating=min_rating,
        max_rating=max_rating,
        release_date_from=release_date_from,
        release_date_to=release_date_to,
        is_active=is_active,
        sort_by=sort_by,
        sort_order=sort_order,
        skip=skip,
        limit=limit,
    )

    return await SearchService.search_content(db, params)
