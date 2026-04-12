from abc import ABC


class LinkErrorMixin(ABC):
    link: str
    """Link to the YouTube video."""


class ProviderErrorMixin(ABC):
    provider: str
    """Tag of the telegram bot that handles the request."""
