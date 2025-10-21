from datetime import UTC, datetime, timedelta
from uuid import UUID

from fastapi import HTTPException, status
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext

from app.auth.schemas import TokenPair
from app.core.config import settings

_pwd_ctx = CryptContext(schemes=['bcrypt'], deprecated='auto')

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = getattr(settings, 'ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = getattr(settings, 'ACCESS_TOKEN_EXPIRE_MINUTES', 30)
REFRESH_TOKEN_EXPIRE_DAYS = getattr(settings, 'REFRESH_TOKEN_EXPIRE_DAYS', 7)


def hash_password(password: str) -> str:
    return _pwd_ctx.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return _pwd_ctx.verify(plain_password, hashed_password)


def create_token_pair(user_id: UUID, remember_me: bool | None) -> TokenPair:
    now = _now()
    access_payload = {
        'sub': str(user_id),
        'type': 'access',
        'iat': _ts(now),
        'exp': _ts(now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)),
    }
    refresh_payload = {
        'sub': str(user_id),
        'type': 'refresh',
        'iat': _ts(now),
        'exp': _ts(now + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)),
    }
    if not remember_me:
        refresh_payload = {
            'sub': str(user_id),
            'type': 'refresh',
            'iat': _ts(now),
            'exp': _ts(now + timedelta(days=1)),
        }
        return TokenPair(
            access_token=jwt.encode(access_payload, SECRET_KEY, algorithm=ALGORITHM),
            refresh_token=jwt.encode(refresh_payload, SECRET_KEY, algorithm=ALGORITHM),
        )

    return TokenPair(
        access_token=jwt.encode(access_payload, SECRET_KEY, algorithm=ALGORITHM),
        refresh_token=jwt.encode(refresh_payload, SECRET_KEY, algorithm=ALGORITHM),
    )


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError as err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='token_expired') from err
    except JWTError as err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid_token') from err


def get_user_from_token(token: str) -> UUID:
    payload = decode_token(token)
    if payload.get('type') != 'access':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid_token_type')
    return UUID(payload.get('sub'))


def refresh_tokens(refresh_token: str) -> TokenPair:
    payload = decode_token(refresh_token)
    if payload.get('type') != 'refresh':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid_token_type')
    return create_token_pair(UUID(payload.get('sub')), True)


def _now() -> datetime:
    return datetime.now(UTC)


def _ts(dt: datetime) -> int:
    return int(dt.timestamp())
