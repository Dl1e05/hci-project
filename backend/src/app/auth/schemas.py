from pydantic import BaseModel, Field


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'


class RefreshInput(BaseModel):
    refresh_token: str


class LoginInput(BaseModel):
    username_or_email: str
    password: str
    is_remember_me: bool = Field(default=False)
