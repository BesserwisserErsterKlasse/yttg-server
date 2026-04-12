from dataclasses import dataclass

from project.server.types.request.base import YttgRequest
from project.server.types.request.enums import YttgCommand


@dataclass(frozen=True)
class SearchRequest(YttgRequest, command=YttgCommand.SEARCH):
    query: str
    """Search term used to retrieve matching YouTube videos."""

    offset: str | None = None
    """
    Opaque pagination token returned by a previous search.
    Used to fetch the next page of results for the same query.
    """
