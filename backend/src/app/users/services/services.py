from uuid import UUID

from fastapi import Depends, HTTPException, status
from pydantic import ValidationError

from app.users.repo import UserRepo, get_user_repo, get_all_active 
from app.users.schemas import UserRead

from typing import List

class GetUsers:
    def __init__(self, repo: UserRepo = Depends(get_user_repo)) -> None:
        self.repo = repo

    async def get_user_by_id(self, user_id: UUID) -> UserRead:
        user = await self.repo.get(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with ID {user_id} not found")
        
        try:
            return UserRead.model_validate(user)
        except ValidationError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error processing user data")
        
    async def get_user_me(self, user_id: UUID) -> UserRead:
        return await self.get_user_by_id(user_id)
    
    async def get_all_active_users(self) -> List[UserRead]:
        users = await self.repo.get_all_active()
        return [UserRead.model_validate(user) for user in users]
