import uuid
from datetime import date

from sqlalchemy import Boolean, CheckConstraint, Date, String, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.base import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=True)
    last_name: Mapped[str] = mapped_column(String(50), nullable=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    phone_number: Mapped[str] = mapped_column(String(15), nullable=True, unique=True)
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('true'))
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))

    __table_args__ = (
        CheckConstraint('char_length(username) >= 3', name='ck_users_username_len'),
        CheckConstraint(
            "email ~* '^[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,}$'",
            name='ck_users_email_format',
        ),
        CheckConstraint("phone_number ~ '^\\+[1-9][0-9]{7,14}$'", name='ck_users_phone_e164'),
        CheckConstraint('birth_date <= CURRENT_DATE', name='ck_users_birth_date_past'),
    )
