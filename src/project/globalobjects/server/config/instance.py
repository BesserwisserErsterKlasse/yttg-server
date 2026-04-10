from pydantic_settings import (
    BaseSettings,
    JsonConfigSettingsSource,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

from project.globalobjects.server.config.protocol import YttgProtocolConfig
from project.globalobjects.server.config.server import TcpServerConfig


class TcpConfig(BaseSettings):
    model_config = SettingsConfigDict(
        json_file='configs/tcp.json',
        extra='forbid',
    )

    server: TcpServerConfig = TcpServerConfig()
    protocol: YttgProtocolConfig = YttgProtocolConfig()

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


tcp_config: TcpConfig = TcpConfig()
