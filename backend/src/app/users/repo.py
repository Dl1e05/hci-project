from collections.abc import Sequence
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

    async def get_all_active(self) -> Sequence[User]:
        res = await self.db.execute(select(User).where(User.is_active))
        return res.scalars().all()

    async def patch(self, user_id: UUID, update_data: dict) -> User | None:
        user = await self.get(user_id)
        if not user:
            return None
        
        for field, value in update_data.items():
            if hasattr(user, field) and value is not None:
                setattr(user, field, value)
        
        await self.db.commit()
        await self.db.refresh(user)
        return user


def get_user_repo(db: AsyncSession = Depends(get_async_session)) -> UserRepo:
    return UserRepo(db)
