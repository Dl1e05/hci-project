from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.core.deps import get_current_user, require_admin, require_user_from_cookie
from app.users.models import User
from app.users.schemas import UserRead, UserUpdate
from app.users.services.services import GetUsers, UpdateUser

router = APIRouter(prefix='/profile', tags=['profile'])


@router.get('/me', response_model=UserRead, status_code=status.HTTP_200_OK, summary='Get current user profile')
async def get_user_me(user_id: UUID = Depends(require_user_from_cookie), services: GetUsers = Depends(GetUsers)) -> UserRead:
    return await services.get_user_me(user_id)


@router.patch('/me', response_model=UserRead, status_code=status.HTTP_200_OK, summary='Partial Update by ID')
async def patch_user_me(
    user_data: UserUpdate, user_id: UUID = Depends(require_user_from_cookie), services: UpdateUser = Depends(UpdateUser)
) -> UserRead:
    return await services.update_user_by_id(user_id, user_data)


@router.get('/active_users', response_model=list[UserRead], status_code=status.HTTP_200_OK, summary='Get all active users')
async def get_all_active_users(
    admin: User = Depends(require_admin),
    services: GetUsers = Depends(GetUsers)
) -> list[UserRead]:
    return await services.get_all_active_users()


@router.get('/{user_id}', response_model=UserRead, status_code=status.HTTP_200_OK, summary='Get user profile by ID')
async def get_user_by_id(
    user_id: UUID, 
    admin: User = Depends(require_admin),
    services: GetUsers = Depends(GetUsers)
) -> UserRead:
    return await services.get_user_by_id(user_id)


@router.patch('/{user_id}', response_model=UserRead, status_code=status.HTTP_200_OK, summary='Partial Update by ID')
async def patch_user_by_id(
    user_id: UUID, 
    user_data: UserUpdate, 
    admin: User = Depends(require_admin),
    services: UpdateUser = Depends(UpdateUser)
) -> UserRead:
    return await services.update_user_by_id(user_id, user_data)
