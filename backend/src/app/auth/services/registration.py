from __future__ import annotations

from fastapi import Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.repo import AuthRepo, get_auth_repo
from app.core.db import get_async_session
from app.core.security import hash_password
from app.users.models import User
from app.users.schemas import UserCreate, UserRead
from app.users.services.errors import classify_integrity_error


class RegistrationService:
    def __init__(self, repo: AuthRepo, db: AsyncSession):
        self.repo = repo
        self.db = db

    async def register(self, data: UserCreate) -> UserRead:
        user = User(
            username=data.username,
            email=data.email,
            birth_date=data.birth_date,
            password=hash_password(data.password.get_secret_value()),
            is_active=True,
        )
        try:
            await self.repo.create(user)
            await self.db.commit()
        except IntegrityError as e:
            await self.db.rollback()
            status, msg = classify_integrity_error(e)
            raise HTTPException(status_code=status, detail=msg) from e

        await self.db.refresh(user)
        return UserRead.model_validate(user)


def get_registration_service(db: AsyncSession = Depends(get_async_session)) -> RegistrationService:
    repo = get_auth_repo(db)
    return RegistrationService(repo=repo, db=db)
