from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.core.deps import require_user_from_cookie
from app.users.schemas import UserRead
from app.users.services.services import GetUsers

router = APIRouter(prefix='/profile', tags=['profile'])


@router.get('/me', response_model=UserRead, status_code=status.HTTP_200_OK, summary='Get current user profile')
async def get_user_me(user_id: UUID = Depends(require_user_from_cookie), services: GetUsers = Depends(GetUsers)) -> UserRead:
    return await services.get_user_me(user_id)


@router.get('/active_users', response_model=list[UserRead], status_code=status.HTTP_200_OK, summary='Get all active users')
async def get_all_active_users(services: GetUsers = Depends(GetUsers)) -> list[UserRead]:
    return await services.get_all_active_users()


@router.get('/{user_id}', response_model=UserRead, status_code=status.HTTP_200_OK, summary='Get user profile by ID')
async def get_user_by_id(user_id: UUID, services: GetUsers = Depends(GetUsers)) -> UserRead:
    return await services.get_user_by_id(user_id)
