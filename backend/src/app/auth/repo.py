from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.users.models import User


class AuthRepo:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get(self, login: str) -> User | None | None:
        stmt = select(User).where((User.username == login) | (User.email == login))
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def create(self, user: User) -> User:
        self.db.add(user)
        await self.db.flush()
        return user


def get_auth_repo(db: AsyncSession = Depends(get_async_session)) -> AuthRepo:
    return AuthRepo(db)
