from uuid import UUID

from fastapi import Depends, HTTPException, status
from pydantic import ValidationError

from app.core.security import hash_password
from app.users.repo import UserRepo, get_user_repo
from app.users.schemas import UserRead, UserUpdate


class GetUsers:
    def __init__(self, repo: UserRepo = Depends(get_user_repo)) -> None:
        self.repo = repo

    async def get_user_by_id(self, user_id: UUID) -> UserRead:
        user = await self.repo.get(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User with ID {user_id} not found')

        try:
            return UserRead.model_validate(user)
        except ValidationError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Error processing user data') from e

    async def get_user_me(self, user_id: UUID) -> UserRead:
        return await self.get_user_by_id(user_id)

    async def get_all_active_users(self) -> list[UserRead]:
        users = await self.repo.get_all_active()
        return [UserRead.model_validate(user) for user in users]


class UpdateUser:
    def __init__(self, repo: UserRepo = Depends(get_user_repo)) -> None:
        self.repo = repo

    async def update_user_by_id(self, user_id: UUID, user_data: UserUpdate) -> UserRead:
        update_dict = user_data.model_dump(exclude_none=True)

        password = update_dict.pop('password', None)

        updated_user = await self.repo.patch(user_id, update_dict)
        if not updated_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with ID {user_id} not found')

        if password is not None:
            updated_user.password = hash_password(password.get_secret_value())
            await self.repo.db.commit()
            await self.repo.db.refresh(updated_user)

        try:
            return UserRead.model_validate(updated_user)
        except ValidationError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Error processing user data') from e
