from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.users.models import User


class UserRepo:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get(self, user_id: UUID) -> User | None | None:
        res = await self.db.execute(select(User).where(User.id == user_id))
        return res.scalar_one_or_none()


def get_user_repo(db: AsyncSession = Depends(get_async_session)) -> UserRepo:
    return UserRepo(db)
