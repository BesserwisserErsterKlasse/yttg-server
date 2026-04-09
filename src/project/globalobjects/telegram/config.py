from pathlib import Path
from typing import ClassVar

from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    JsonConfigSettingsSource,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

from modules.telegram import Proxy


class TelegramConfig(BaseSettings):
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        extra='forbid',
        strict=True,
        validate_default=True,
        json_file='configs/telegram.json',
    )

    language_code: str = Field(default='en', min_length=2, max_length=2)
    """Interface language used by Telegram server responses."""

    ipv6: bool = Field(default=False)
    """Whether to use IPv6."""

    proxy: Proxy | None = Field(default=None)
    """Proxy to route the traffic through."""

    workers: int = Field(default=4)
    """Maximum number of concurrent workers for handling incoming updates."""

    workdir: Path = Field(default=Path('session'))
    """Path to the folder where the session files should reside."""

    sleep_threshold: int = Field(default=30, ge=0)
    """
    Threshold in seconds for handling FloodWait errors.
        - If wait_time <= FloodSleepThreshold -> sleep automatically.
        - If wait_time > FloodSleepThreshold -> raise FloodWait exception.
    """

    hide_password: bool = Field(default=True)
    """Whether to hide 2FA password."""

    max_concurrent_transmissions: int = Field(default=4)
    """Maximum number of concurrent uploads & downloads."""

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[
        PydanticBaseSettingsSource,
        JsonConfigSettingsSource,
        PydanticBaseSettingsSource,
        PydanticBaseSettingsSource,
        PydanticBaseSettingsSource,
    ]:
        return (
            init_settings,
            JsonConfigSettingsSource(settings_cls),
            env_settings,
            dotenv_settings,
            file_secret_settings,
        )


telegram_config: TelegramConfig = TelegramConfig()
