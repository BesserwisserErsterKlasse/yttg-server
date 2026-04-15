from dataclasses import dataclass

from project.server.types.response.base import YttgResponse


@dataclass(frozen=True)
class BackgroundResponse(YttgResponse):
    pass
