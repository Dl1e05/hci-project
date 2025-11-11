from typing import TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.content.models.base import BaseContent

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
