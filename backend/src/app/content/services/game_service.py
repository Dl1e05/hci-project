from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.content.models.content import Game
from app.content.repo import ContentRepository
from app.content.schemas.content import GameCreate, GameRead, GameUpdate


class GameService:
    @staticmethod
    async def create(db: AsyncSession, game_data: GameCreate) -> GameRead:
        data = game_data.model_dump()
        game = await ContentRepository.create(db, Game, data)
        return GameRead.model_validate(game)

    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[GameRead]:
        games = await ContentRepository.get_all(db, Game, skip, limit)
        return [GameRead.model_validate(game) for game in games]

    @staticmethod
    async def get_by_id(db: AsyncSession, game_id: UUID) -> GameRead | None:
        game = await ContentRepository.get_by_id(db, Game, game_id)
        return GameRead.model_validate(game) if game else None

    @staticmethod
    async def update(db: AsyncSession, game_id: UUID, game_data: GameUpdate) -> GameRead | None:
        data = game_data.model_dump(exclude_unset=True)
        game = await ContentRepository.update(db, Game, game_id, data)
        return GameRead.model_validate(game) if game else None

    @staticmethod
    async def delete(db: AsyncSession, game_id: UUID) -> bool:
        return await ContentRepository.delete(db, Game, game_id)

