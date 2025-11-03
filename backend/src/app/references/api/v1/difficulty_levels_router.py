from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED

from app.references.schemas import DifficultyLevelCreate, DifficultyLevelRead, DifficultyLevelUpdate
from app.references.services.difficulty_level_service import DifficultyLevelService
from app.core.db import get_async_session

router = APIRouter(prefix='/content')


@router.post('/difficulty-levels', response_model=DifficultyLevelRead, status_code=HTTP_201_CREATED, tags=['difficulty-levels'])
async def create_difficulty_level(difficulty_data: DifficultyLevelCreate, db: AsyncSession = Depends(get_async_session)) -> DifficultyLevelRead:
    existing_difficulty = await DifficultyLevelService.get_by_level(db, difficulty_data.level)
    if existing_difficulty:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Difficulty level '{difficulty_data.level}' already exists"
        )
    return await DifficultyLevelService.create(db, difficulty_data)


@router.get('/difficulty-levels', response_model=list[DifficultyLevelRead], tags=['difficulty-levels'])
async def get_all_difficulty_levels(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_session)) -> list[DifficultyLevelRead]:
    return await DifficultyLevelService.get_all(db, skip=skip, limit=limit)


@router.get('/difficulty-levels/{difficulty_id}', response_model=DifficultyLevelRead, tags=['difficulty-levels'])
async def get_difficulty_level(difficulty_id: int, db: AsyncSession = Depends(get_async_session)) -> DifficultyLevelRead:
    difficulty = await DifficultyLevelService.get_by_id(db, difficulty_id)
    if not difficulty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Difficulty level with id {difficulty_id} not found')
    return difficulty


@router.patch('/difficulty-levels/{difficulty_id}', response_model=DifficultyLevelRead, tags=['difficulty-levels'])
async def update_difficulty_level(difficulty_id: int, difficulty_data: DifficultyLevelUpdate, db: AsyncSession = Depends(get_async_session)) -> DifficultyLevelRead:
    if difficulty_data.level:
        existing_difficulty = await DifficultyLevelService.get_by_level(db, difficulty_data.level)
        if existing_difficulty and existing_difficulty.id != difficulty_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Difficulty level '{difficulty_data.level}' already exists"
            )

    difficulty = await DifficultyLevelService.update(db, difficulty_id, difficulty_data)
    if not difficulty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Difficulty level with id {difficulty_id} not found')
    return difficulty


@router.delete('/difficulty-levels/{difficulty_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['difficulty-levels'])
async def delete_difficulty_level(difficulty_id: int, db: AsyncSession = Depends(get_async_session)) -> None:
    deleted = await DifficultyLevelService.delete(db, difficulty_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Difficulty level with id {difficulty_id} not found')

