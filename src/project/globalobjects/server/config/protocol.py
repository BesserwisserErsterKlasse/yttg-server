from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field


class YttgProtocolConfig(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(
        extra='forbid',
        strict=True,
        validate_default=True,
    )

    header_size: int = Field(default=16, ge=2)
    """Size in bytes of the YTTG protocol header."""
