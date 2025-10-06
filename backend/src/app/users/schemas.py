from __future__ import annotations

from datetime import date
from typing import Annotated
from uuid import UUID

from pydantic import EmailStr, Field, SecretStr, field_validator, model_validator
from pydantic.types import StringConstraints

from app.base import ORMModel

Username = Annotated[str, StringConstraints(min_length=3, max_length=50)]
Name50 = Annotated[str, StringConstraints(min_length=1, max_length=50)]
OptName50 = Annotated[str | None, StringConstraints(min_length=1, max_length=50)]
PhoneE164 = Annotated[str, StringConstraints(pattern=r'^\+[1-9]\d{7,14}$', max_length=16)]
Password = Annotated[SecretStr, StringConstraints(min_length=8)]


class UserBase(ORMModel):
    username: Username
    email: EmailStr
    birth_date: date

    @field_validator('email')
    @classmethod
    def norm_email(cls, v: str) -> str:
        return v.strip().lower()

    @field_validator('username')
    @classmethod
    def norm_username(cls, v: str) -> str:
        return v.strip()


class UserCreate(UserBase):
    password: Password
    password_repeat: Password

    @model_validator(mode='after')
    def password_match(self) -> UserCreate:
        if self.password.get_secret_value() != self.password_repeat.get_secret_value():
            raise ValueError("Passwords don't match")
        return self


class UserUpdate(ORMModel):
    username: Annotated[str | None, StringConstraints(min_length=3, max_length=50)] = None
    first_name: OptName50 = None
    last_name: OptName50 = None
    email: EmailStr | None = None
    phone_number: PhoneE164 | None = None
    birth_date: date | None = None
    password: Password | None = None
    password_repeat: Password | None = None

    @model_validator(mode='after')
    def passwords_match(self) -> UserUpdate:
        p1 = self.password.get_secret_value() if self.password is not None else None
        p2 = self.password_repeat.get_secret_value() if self.password_repeat is not None else None

        if (p1 is None) ^ (p2 is None):
            raise ValueError('Both password and password_repeat are required to change password')
        if p1 is not None and p1 != p2:
            raise ValueError("Passwords don't match")
        return self


class UserRead(UserBase):
    id: UUID
    is_active: bool = Field(default=True)
