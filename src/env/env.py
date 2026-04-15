from typing import Annotated, ClassVar, Final, Literal

from pydantic import BaseModel, BeforeValidator, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

type ML_KEM = Annotated[
    Literal[512, 768, 1024],
    BeforeValidator(lambda v: int(v) if isinstance(v, str) else v),
]


class TelegramSettings(BaseModel):
    api_id: int
    """Telegram app API id."""

    api_hash: str = Field(pattern=r'[0-9a-f]{32}')
    """Telegram app API hash."""


class CryptoSettings(BaseModel):
    pre_shared_secret: bytes
    """Pre-shared secret for public key exchange."""

    ml_kem: ML_KEM = Field(default=512)
    """MK-KEM standard."""


class Env(BaseSettings):
    telegram: TelegramSettings
    crypto: CryptoSettings

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_file='.env',
        env_nested_delimiter='__',
    )


env: Final[Env] = Env()
"""Environment variables."""
