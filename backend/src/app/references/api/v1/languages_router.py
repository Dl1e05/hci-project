from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED

from app.references.schemas import LanguageCreate, LanguageRead, LanguageUpdate
from app.references.services.language_service import LanguageService
from app.core.db import get_async_session

router = APIRouter(prefix='/content')


@router.post('/languages', response_model=LanguageRead, status_code=HTTP_201_CREATED, tags=['languages'])
async def create_language(language_data: LanguageCreate, db: AsyncSession = Depends(get_async_session)) -> LanguageRead:
    existing_language = await LanguageService.get_by_code(db, language_data.code)
    if existing_language:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Language with code '{language_data.code}' already exists"
        )
    return await LanguageService.create(db, language_data)


@router.get('/languages', response_model=list[LanguageRead], tags=['languages'])
async def get_all_languages(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_session)) -> list[LanguageRead]:
    return await LanguageService.get_all(db, skip=skip, limit=limit)


@router.get('/languages/{language_id}', response_model=LanguageRead, tags=['languages'])
async def get_language(language_id: int, db: AsyncSession = Depends(get_async_session)) -> LanguageRead:
    language = await LanguageService.get_by_id(db, language_id)
    if not language:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Language with id {language_id} not found')
    return language


@router.patch('/languages/{language_id}', response_model=LanguageRead, tags=['languages'])
async def update_language(language_id: int, language_data: LanguageUpdate, db: AsyncSession = Depends(get_async_session)) -> LanguageRead:
    if language_data.code:
        existing_language = await LanguageService.get_by_code(db, language_data.code)
        if existing_language and existing_language.id != language_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Language with code '{language_data.code}' already exists"
            )

    language = await LanguageService.update(db, language_id, language_data)
    if not language:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Language with id {language_id} not found')
    return language


@router.delete('/languages/{language_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['languages'])
async def delete_language(language_id: int, db: AsyncSession = Depends(get_async_session)) -> None:
    deleted = await LanguageService.delete(db, language_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Language with id {language_id} not found')

