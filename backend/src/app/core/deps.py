from uuid import UUID

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.security import decode_token
from app.users.models import User
from app.users.repo import UserRepo

bearer = HTTPBearer(bearerFormat='JWT')


def require_user_from_cookie(request: Request) -> UUID:
    token = request.cookies.get('access_token')
    if not token:
        raise HTTPException(status_code=401, detail='Not authenticated')

    payload = decode_token(token)
    sub = payload.get('sub')
    if not sub:
        raise HTTPException(status_code=404, detail='Not Found')
    try:
        return UUID(sub)
    except ValueError as e:
        raise HTTPException(status_code=401, detail='Invalid subject format') from e

async def get_current_user(
        user_id: UUID = Depends(require_user_from_cookie),
        db: AsyncSession = Depends(get_async_session)
) -> User:
    repo = UserRepo(db)
    user = await repo.get(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='User account is deactivated'
        )
    
    return user

async def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Administrator privileges required"
        )
    
    return current_user