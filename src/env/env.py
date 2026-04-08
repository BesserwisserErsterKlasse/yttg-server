from typing import ClassVar, Final

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class TelegramSettings(BaseModel):
    api_id: int
    """Telegram app API id."""

    api_hash: str = Field(pattern=r'[0-9a-f]{32}')
    """Telegram app API hash."""


class Env(BaseSettings):
    telegram: TelegramSettings

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_file='.env',
        env_nested_delimiter='__',
    )


env: Final[Env] = Env()
"""Environment variables."""
