from __future__ import annotations

from fastapi import Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.repo import AuthRepo, get_auth_repo
from app.core.db import get_async_session
from app.core.security import hash_password
from app.users.models import User
from app.users.schemas import UserCreate, UserRead


class RegistrationService:
    def __init__(self, repo: AuthRepo, db: AsyncSession):
        self.repo = repo
        self.db = db

    async def register(self, data: UserCreate) -> UserRead:
        user = User(
            username=data.username,
            first_name=data.first_name,
            last_name=data.last_name,
            password=hash_password(data.password.get_secret_value()),
            email=data.email,
            is_active=True,
        )
        try:
            await self.repo.create(user)
            await self.db.commit()
        except IntegrityError as e:
            await self.db.rollback()
            msg = "User already exists"
            if "users_username_key" in str(e.orig):
                msg = "Username already exists"
            elif "users_email_key" in str(e.orig):
                msg = "Email already exists"
            raise HTTPException(status_code=400, detail=msg) from e

        await self.db.refresh(user)
        return UserRead.model_validate(user)


def get_registration_service(
    repo: AuthRepo = Depends(get_auth_repo), db: AsyncSession = Depends(get_async_session)
) -> RegistrationService:
    return RegistrationService(repo=repo, db=db)