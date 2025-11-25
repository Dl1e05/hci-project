from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.content.models.base import BaseContent
from app.content.schemas.search import ContentSearchParams, ContentSearchResult


class SearchService:
    @staticmethod
    async def search_content(db: AsyncSession, params: ContentSearchParams) -> ContentSearchResult:
        query = select(BaseContent).options(
            selectinload(BaseContent.genres),
            selectinload(BaseContent.audio_languages),
            selectinload(BaseContent.subtitle_languages),
            selectinload(BaseContent.content_tags),
            selectinload(BaseContent.original_language),
            selectinload(BaseContent.age_rating),
            selectinload(BaseContent.original_author),
            selectinload(BaseContent.country),
            selectinload(BaseContent.difficulty_level),
        )

        conditions = []

        if params.search:
            search_pattern = f'%{params.search}%'
            conditions.append(
                or_(
                    BaseContent.title.ilike(search_pattern),
                    BaseContent.short_description.ilike(search_pattern),
                    BaseContent.long_description.ilike(search_pattern),
                    BaseContent.keywords.ilike(search_pattern),
                )
            )

        if params.title:
            conditions.append(BaseContent.title.ilike(f'%{params.title}%'))

        if params.short_description:
            conditions.append(BaseContent.short_description.ilike(f'%{params.short_description}%'))

        if params.long_description:
            conditions.append(BaseContent.long_description.ilike(f'%{params.long_description}%'))

        if params.keywords:
            conditions.append(BaseContent.keywords.ilike(f'%{params.keywords}%'))

        if params.content_types:
            conditions.append(BaseContent.content_type.in_(params.content_types))

        if params.genre_ids:
            from app.references.models import Genres

            query = query.join(BaseContent.genres).where(Genres.id.in_(params.genre_ids))

        if params.tag_ids:
            from app.references.models import Tags

            query = query.join(BaseContent.content_tags).where(Tags.id.in_(params.tag_ids))

        if params.audio_language_ids:
            from app.references.models import Language

            query = query.join(BaseContent.audio_languages).where(Language.id.in_(params.audio_language_ids))

        if params.subtitle_language_ids:
            from app.references.models import Language

            query = query.join(BaseContent.subtitle_languages).where(Language.id.in_(params.subtitle_language_ids))

        if params.original_language_id is not None:
            conditions.append(BaseContent.original_language_id == params.original_language_id)

        if params.age_rating_id is not None:
            conditions.append(BaseContent.age_rating_id == params.age_rating_id)

        if params.author_id is not None:
            conditions.append(BaseContent.original_author_id == params.author_id)

        if params.country_id is not None:
            conditions.append(BaseContent.country_id == params.country_id)

        if params.difficulty_level_id is not None:
            conditions.append(BaseContent.difficulty_level_id == params.difficulty_level_id)

        if params.min_rating is not None:
            conditions.append(BaseContent._rating >= params.min_rating)

        if params.max_rating is not None:
            conditions.append(BaseContent._rating <= params.max_rating)

        if params.release_date_from is not None:
            conditions.append(BaseContent.release_date >= params.release_date_from)

        if params.release_date_to is not None:
            conditions.append(BaseContent.release_date <= params.release_date_to)

        if params.is_active is not None:
            conditions.append(BaseContent.is_active == params.is_active)

        if conditions:
            query = query.where(and_(*conditions))

        count_query = select(BaseContent.id)
        if conditions:
            count_query = count_query.where(and_(*conditions))

        total_result = await db.execute(count_query)
        total = len(total_result.all())

        if params.sort_by:
            sort_column = getattr(BaseContent, params.sort_by, None)
            if sort_column is not None:
                query = (
                    query.order_by(sort_column.asc())
                    if params.sort_order == 'asc'
                    else query.order_by(sort_column.desc())
                )
        else:
            query = query.order_by(BaseContent.created_at.desc())

        query = query.offset(params.skip).limit(params.limit)

        result = await db.execute(query)
        items = list(result.scalars().unique().all())

        return ContentSearchResult(items=items, total=total, skip=params.skip, limit=params.limit)