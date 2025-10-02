from uuid import UUID

from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer

from app.core.security import decode_token

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
