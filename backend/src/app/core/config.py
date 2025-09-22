# src/app/core/config.py
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import make_url

ROOT_DIR = Path(__file__).resolve().parents[3]
ENV_PATH = ROOT_DIR / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    DEBUG: bool = Field(default=False, alias="DEBUG")
    DATABASE_URL: str = Field(..., alias="DATABASE_URL")
    SECRET_KEY: str = Field(..., alias="SECRET_KEY")

    @property
    def SYNC_DATABASE_URL(self) -> str:
        u = make_url(self.DATABASE_URL)
        return str(u.set(drivername="postgresql+psycopg2"))


settings = Settings()
