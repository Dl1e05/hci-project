from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.references.models import Language
from app.references.schemas import LanguageCreate, LanguageRead, LanguageUpdate


class LanguageService:
    @staticmethod
    async def create(db: AsyncSession, language_data: LanguageCreate) -> LanguageRead:
        language = Language(**language_data.model_dump())
        db.add(language)
        await db.commit()
        await db.refresh(language)
        return LanguageRead.model_validate(language)

    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[LanguageRead]:
        result = await db.execute(select(Language).offset(skip).limit(limit).order_by(Language.name))
        languages = result.scalars().all()
        return [LanguageRead.model_validate(language) for language in languages]

    @staticmethod
    async def get_by_id(db: AsyncSession, language_id: int) -> LanguageRead | None:
        result = await db.execute(select(Language).where(Language.id == language_id))
        language = result.scalar_one_or_none()
        return LanguageRead.model_validate(language) if language else None

    @staticmethod
    async def get_by_code(db: AsyncSession, code: str) -> Language | None:
        result = await db.execute(select(Language).where(Language.code == code))
        return result.scalar_one_or_none()

    @staticmethod
    async def update(db: AsyncSession, language_id: int, language_data: LanguageUpdate) -> LanguageRead | None:
        result = await db.execute(select(Language).where(Language.id == language_id))
        language_entity = result.scalar_one_or_none()
        if not language_entity:
            return None

        update_data = language_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(language_entity, field, value)

        await db.commit()
        await db.refresh(language_entity)
        return LanguageRead.model_validate(language_entity)

    @staticmethod
    async def delete(db: AsyncSession, language_id: int) -> bool:
        result = await db.execute(select(Language).where(Language.id == language_id))
        language_entity = result.scalar_one_or_none()
        if not language_entity:
            return False

        await db.delete(language_entity)
        await db.commit()
        return True

