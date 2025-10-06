from fastapi import Depends, HTTPException

from app.auth.repo import AuthRepo, get_auth_repo
from app.auth.schemas import LoginInput, TokenPair
from app.core.security import create_token_pair, verify_password


class LoginService:
    def __init__(self, repo: AuthRepo = Depends(get_auth_repo)) -> None:
        self.repo = repo

    async def login(self, data: LoginInput) -> TokenPair:
        login = data.username_or_email
        remember_me = data.is_remember_me

        user = await self.repo.get(login)

        if not user or not verify_password(data.password, user.password):
            raise HTTPException(status_code=401, detail='User does not exist or password is incorrect')

        return create_token_pair(user.id, remember_me)
