from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED

from app.content.schemas.content import GameCreate, GameRead, GameUpdate
from app.content.services.game_service import GameService
from app.core.db import get_async_session

router = APIRouter(prefix='/content')


@router.post('/games', response_model=GameRead, status_code=HTTP_201_CREATED, tags=['games'])
async def create_game(game_data: GameCreate, db: AsyncSession = Depends(get_async_session)) -> GameRead:
    try:
        return await GameService.create(db, game_data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.get('/games', response_model=list[GameRead], tags=['games'])
async def get_all_games(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_session)) -> list[GameRead]:
    return await GameService.get_all(db, skip=skip, limit=limit)


@router.get('/games/{game_id}', response_model=GameRead, tags=['games'])
async def get_game(game_id: UUID, db: AsyncSession = Depends(get_async_session)) -> GameRead:
    game = await GameService.get_by_id(db, game_id)
    if not game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Game with id {game_id} not found')
    return game


@router.patch('/games/{game_id}', response_model=GameRead, tags=['games'])
async def update_game(game_id: UUID, game_data: GameUpdate, db: AsyncSession = Depends(get_async_session)) -> GameRead:
    game = await GameService.update(db, game_id, game_data)
    if not game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Game with id {game_id} not found')
    return game


@router.delete('/games/{game_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['games'])
async def delete_game(game_id: UUID, db: AsyncSession = Depends(get_async_session)) -> None:
    deleted = await GameService.delete(db, game_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Game with id {game_id} not found')

