from uuid import UUID

from fastapi import Depends, HTTPException, status

from app.users.repo import UserRepo, get_user_repo
from app.users.schemas import UserRead


class GetUsers:
    def __init__(self, repo: UserRepo = Depends(get_user_repo)) -> None:
        self.repo = repo

    async def get_user_me(self, user_id: UUID) -> UserRead:
        user = await self.repo.get(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserRead.model_validate(user)
