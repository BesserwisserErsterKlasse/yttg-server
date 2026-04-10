from re import compile, Pattern, RegexFlag
from typing import ClassVar, Final

from pydantic import BaseModel, ConfigDict, Field

IPv4: Final[Pattern[str]] = compile(
    pattern=r'''
        ^(
            localhost
            |
            (?:
                (?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)
                \.
                (?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)
                \.
                (?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)
                \.
                (?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)
            )
        )$
    ''',
    flags=RegexFlag.VERBOSE,
)


class TcpServerConfig(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(
        extra='forbid',
        strict=True,
        validate_default=True,
    )

    host: str = Field(default='localhost', pattern=IPv4)
    """IP address the server binds to."""

    port: int = Field(default=21027, ge=1024, le=65535)
    """Port which the server listens on."""

    max_connections: int = Field(default=128, ge=1)
    """Maximum number of connections to the server."""
