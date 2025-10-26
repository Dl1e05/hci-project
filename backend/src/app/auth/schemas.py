from pydantic import BaseModel, Field, field_validator


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'


class RefreshInput(BaseModel):
    refresh_token: str


class LoginInput(BaseModel):
    username_or_email: str = Field(min_length=1, description="Username or email is required")
    password: str = Field(min_length=1, description="Password is required")
    is_remember_me: bool = Field(default=False)

    @field_validator('username_or_email')
    @classmethod
    def validate_username_or_email(cls, v):
        if not v or not v.strip():
            raise ValueError('Username or email cannot be empty')
        return v.strip()

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if not v or not v.strip():
            raise ValueError('Password cannot be empty')
        return v.strip()
