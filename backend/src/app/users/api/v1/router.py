from uuid import UUID

from fastapi import APIRouter, Depends, status
from app.users.schemas import UserRead
from app.users.services.services import GetUsers
from app.core.deps import require_user_from_cookie

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("/me", response_model=UserRead, status_code=status.HTTP_200_OK, summary="Get current user profile")
async def get_user_me(user_id: UUID = Depends(require_user_from_cookie), services: GetUsers = Depends(GetUsers)) -> UserRead:
    return await services.get_user_me(user_id)
