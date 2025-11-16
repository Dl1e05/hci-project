from typing import Any, TypeVar
from uuid import UUID

from sqlalchemy import Select, and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.content.models.base import BaseContent
from app.content.schemas.filters import ContentFilterParams

T = TypeVar('T', bound=BaseContent)


def _convert_url_fields(data: dict) -> dict:
    """Convert HttpUrl objects to strings for database storage"""
    url_fields = ['banner', 'trailer', 'link']
    for field in url_fields:
        if field in data and data[field] is not None:
            data[field] = str(data[field])
    return data


class ContentRepository:
    """Base repository for content operations"""

    @staticmethod
    async def create(db: AsyncSession, model_class: type[T], data: dict) -> T:
        """Create a new content instance"""
        # Convert URL fields to strings
        data = _convert_url_fields(data)

        # Separate relationship data
        genre_ids = data.pop('genre_ids', [])
        audio_language_ids = data.pop('audio_language_ids', [])
        subtitle_language_ids = data.pop('subtitle_language_ids', [])
        tag_ids = data.pop('tag_ids', [])

        # Create the content instance
        content = model_class(**data)
        db.add(content)

        # Handle relationships if IDs are provided
        if genre_ids:
            from app.references.models import Genres

            genres_result = await db.execute(select(Genres).where(Genres.id.in_(genre_ids)))
            genres_list: list[Genres] = list(genres_result.scalars().all())
            content.genres = genres_list

        if audio_language_ids:
            from app.references.models import Language

            audio_langs_result = await db.execute(select(Language).where(Language.id.in_(audio_language_ids)))
            audio_languages_list: list[Language] = list(audio_langs_result.scalars().all())
            content.audio_languages = audio_languages_list

        if subtitle_language_ids:
            from app.references.models import Language

            subtitle_langs_result = await db.execute(select(Language).where(Language.id.in_(subtitle_language_ids)))
            subtitle_languages_list: list[Language] = list(subtitle_langs_result.scalars().all())
            content.subtitle_languages = subtitle_languages_list

        if tag_ids:
            from app.references.models import Tags

            tags_result = await db.execute(select(Tags).where(Tags.id.in_(tag_ids)))
            tags_list: list[Tags] = list(tags_result.scalars().all())
            content.content_tags = tags_list

        await db.commit()
        await db.refresh(content, attribute_names=['genres', 'audio_languages', 'subtitle_languages', 'content_tags'])
        return content

    @staticmethod
    async def get_all(db: AsyncSession, model_class: type[T], skip: int = 0, limit: int = 100) -> list[T]:
        """Get all content of a specific type"""
        result = await db.execute(
            select(model_class)
            .options(
                selectinload(model_class.genres),
                selectinload(model_class.audio_languages),
                selectinload(model_class.subtitle_languages),
                selectinload(model_class.content_tags),
                selectinload(model_class.original_language),
                selectinload(model_class.age_rating),
                selectinload(model_class.original_author),
                selectinload(model_class.country),
            )
            .offset(skip)
            .limit(limit)
            .order_by(model_class.created_at.desc())
        )
        return list(result.scalars().all())

    @staticmethod
    async def get_by_id(db: AsyncSession, model_class: type[T], content_id: UUID) -> T | None:
        """Get content by ID"""
        result = await db.execute(
            select(model_class)
            .options(
                selectinload(model_class.genres),
                selectinload(model_class.audio_languages),
                selectinload(model_class.subtitle_languages),
                selectinload(model_class.content_tags),
                selectinload(model_class.original_language),
                selectinload(model_class.age_rating),
                selectinload(model_class.original_author),
                selectinload(model_class.country),
            )
            .where(model_class.id == content_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def update(db: AsyncSession, model_class: type[T], content_id: UUID, data: dict) -> T | None:
        """Update content"""
        # Fetch the content
        result = await db.execute(
            select(model_class)
            .options(
                selectinload(model_class.genres),
                selectinload(model_class.audio_languages),
                selectinload(model_class.subtitle_languages),
                selectinload(model_class.content_tags),
                selectinload(model_class.original_language),
                selectinload(model_class.age_rating),
                selectinload(model_class.original_author),
                selectinload(model_class.country),
            )
            .where(model_class.id == content_id)
        )
        content = result.scalar_one_or_none()
        if not content:
            return None

        # Convert URL fields to strings
        data = _convert_url_fields(data)

        # Separate relationship data
        genre_ids = data.pop('genre_ids', None)
        audio_language_ids = data.pop('audio_language_ids', None)
        subtitle_language_ids = data.pop('subtitle_language_ids', None)
        tag_ids = data.pop('tag_ids', None)

        # Update scalar fields
        for field, value in data.items():
            setattr(content, field, value)

        # Update relationships if provided
        if genre_ids is not None:
            from app.references.models import Genres

            genres_result = await db.execute(select(Genres).where(Genres.id.in_(genre_ids)))
            genres_list: list[Genres] = list(genres_result.scalars().all())
            content.genres = genres_list

        if audio_language_ids is not None:
            from app.references.models import Language

            audio_langs_result = await db.execute(select(Language).where(Language.id.in_(audio_language_ids)))
            audio_languages_list: list[Language] = list(audio_langs_result.scalars().all())
            content.audio_languages = audio_languages_list

        if subtitle_language_ids is not None:
            from app.references.models import Language

            subtitle_langs_result = await db.execute(select(Language).where(Language.id.in_(subtitle_language_ids)))
            subtitle_languages_list: list[Language] = list(subtitle_langs_result.scalars().all())
            content.subtitle_languages = subtitle_languages_list

        if tag_ids is not None:
            from app.references.models import Tags

            tags_result = await db.execute(select(Tags).where(Tags.id.in_(tag_ids)))
            tags_list: list[Tags] = list(tags_result.scalars().all())
            content.content_tags = tags_list

        await db.commit()
        await db.refresh(content, attribute_names=['genres', 'audio_languages', 'subtitle_languages', 'content_tags'])
        return content

    @staticmethod
    async def delete(db: AsyncSession, model_class: type[T], content_id: UUID) -> bool:
        """Delete content"""
        result = await db.execute(select(model_class).where(model_class.id == content_id))
        content = result.scalar_one_or_none()
        if not content:
            return False

        await db.delete(content)
        await db.commit()
        return True

    @staticmethod
    def _apply_base_filters(query: Select[tuple[T]], model_class: type[T], filters: ContentFilterParams) -> Select[tuple[T]]:
        """Apply base content filters to query"""
        from app.references.models import Genres, Language, Tags

        conditions = []

        # Search across multiple text fields
        if filters.search:
            search_pattern = f'%{filters.search}%'
            conditions.append(
                or_(
                    model_class.title.ilike(search_pattern),
                    model_class.short_description.ilike(search_pattern),
                    model_class.long_description.ilike(search_pattern),
                    model_class.keywords.ilike(search_pattern),
                )
            )

        # Filter by relationships using joins
        if filters.genre_ids:
            query = query.join(model_class.genres).where(Genres.id.in_(filters.genre_ids))

        if filters.tag_ids:
            query = query.join(model_class.content_tags).where(Tags.id.in_(filters.tag_ids))

        if filters.audio_language_ids:
            query = query.join(model_class.audio_languages).where(Language.id.in_(filters.audio_language_ids))

        if filters.subtitle_language_ids:
            query = query.join(model_class.subtitle_languages).where(Language.id.in_(filters.subtitle_language_ids))

        # Filter by scalar fields
        if filters.original_language_id is not None:
            conditions.append(model_class.original_language_id == filters.original_language_id)

        if filters.age_rating_id is not None:
            conditions.append(model_class.age_rating_id == filters.age_rating_id)

        if filters.author_id is not None:
            conditions.append(model_class.original_author_id == filters.author_id)

        if filters.country_id is not None:
            conditions.append(model_class.country_id == filters.country_id)

        if filters.min_rating is not None:
            conditions.append(model_class._rating >= filters.min_rating)

        if filters.max_rating is not None:
            conditions.append(model_class._rating <= filters.max_rating)

        if filters.release_date_from is not None:
            conditions.append(model_class.release_date >= filters.release_date_from)

        if filters.release_date_to is not None:
            conditions.append(model_class.release_date <= filters.release_date_to)

        if filters.is_active is not None:
            conditions.append(model_class.is_active == filters.is_active)

        if conditions:
            query = query.where(and_(*conditions))

        return query

    @staticmethod
    def _apply_sorting(query: Select[tuple[T]], model_class: type[T], filters: ContentFilterParams) -> Select[tuple[T]]:
        """Apply sorting to query"""
        if filters.sort_by:
            sort_column = getattr(model_class, filters.sort_by, None)
            if sort_column is not None:
                query = query.order_by(sort_column.asc()) if filters.sort_order == 'asc' else query.order_by(sort_column.desc())
        else:
            # Default sorting by created_at desc if no sort specified
            query = query.order_by(model_class.created_at.desc())

        return query

    @staticmethod
    async def get_filtered(
        db: AsyncSession,
        model_class: type[T],
        filters: ContentFilterParams,
        skip: int = 0,
        limit: int = 100,
        additional_filters: dict[str, Any] | None = None,
    ) -> tuple[list[T], int]:
        """Get filtered and paginated content with total count

        Args:
            db: Database session
            model_class: Content model class
            filters: Base content filters
            skip: Number of records to skip
            limit: Maximum number of records to return
            additional_filters: Additional model-specific filters (e.g., for Book, Film, etc.)

        Returns:
            Tuple of (list of content items, total count)
        """
        # Build base query with relationships
        query = select(model_class).options(
            selectinload(model_class.genres),
            selectinload(model_class.audio_languages),
            selectinload(model_class.subtitle_languages),
            selectinload(model_class.content_tags),
            selectinload(model_class.original_language),
            selectinload(model_class.age_rating),
            selectinload(model_class.original_author),
            selectinload(model_class.country),
        )

        # Apply base content filters
        query = ContentRepository._apply_base_filters(query, model_class, filters)

        # Apply additional model-specific filters
        if additional_filters:
            conditions = []
            for field, value in additional_filters.items():
                if value is not None:
                    column = getattr(model_class, field, None)
                    if column is not None:
                        if isinstance(value, dict):
                            # Handle range filters like {'min': 1, 'max': 100}
                            if 'min' in value and value['min'] is not None:
                                conditions.append(column >= value['min'])
                            if 'max' in value and value['max'] is not None:
                                conditions.append(column <= value['max'])
                        elif isinstance(value, str) and hasattr(column, 'ilike'):
                            # Handle string partial match filters
                            conditions.append(column.ilike(f'%{value}%'))
                        else:
                            # Handle exact match filters
                            conditions.append(column == value)

            if conditions:
                query = query.where(and_(*conditions))

        # Get total count before pagination
        count_query = select(func.count()).select_from(query.distinct().subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar_one()

        # Apply sorting
        query = ContentRepository._apply_sorting(query, model_class, filters)

        # Apply pagination
        query = query.offset(skip).limit(limit)

        # Execute query
        result = await db.execute(query)
        items = list(result.scalars().all())

        return items, total
