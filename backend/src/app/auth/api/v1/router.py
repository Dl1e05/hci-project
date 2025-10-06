from fastapi import APIRouter, Depends, Response, status

from app.auth.schemas import LoginInput, TokenPair
from app.auth.services.login import LoginService
from app.auth.services.registration import RegistrationService, get_registration_service
from app.users.schemas import UserCreate, UserRead

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/register', response_model=UserRead, status_code=status.HTTP_201_CREATED, summary='New user registration')
async def register(user: UserCreate, service: RegistrationService = Depends(get_registration_service)) -> UserRead:  # noqa: B008
    return await service.register(user)


@router.post('/login', response_model=TokenPair, status_code=status.HTTP_200_OK, summary='Login with JWT receive')
async def login(data: LoginInput, response: Response, service: LoginService = Depends(LoginService)) -> TokenPair:  # noqa: B008
    token_pair = await service.login(data)
    refresh_max_age = 60 * 60 * 24 * 7 if data.is_remember_me else 60 * 60 * 24

    _set_auth_cookies(response, token_pair.access_token, token_pair.refresh_token, refresh_max_age)

    return token_pair

def _set_auth_cookies(response: Response, access_token: str, refresh_token: str, refresh_max_age: int) -> None:
    response.set_cookie(
        key='access_token',
        value=access_token,
        httponly=True,
        secure=False,
        samesite='lax',
        max_age=3600
    )

    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite='lax',
        max_age=refresh_max_age
    )

