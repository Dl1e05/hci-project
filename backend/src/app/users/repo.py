from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.app.core.db import get_async_session
from src.app.users.models import User


class UserRepo:
    def __init__(self, db=AsyncSession):
        self.db = db

    async def get(self, user_id: UUID) -> User | None | None:
        res = await self.db.execute(select(User).where(User.id == user_id))
        return res.scalars_one_or_none()


def get_user_repo(db: AsyncSession = Depends(get_async_session)) -> UserRepo:
    return UserRepo(db)
