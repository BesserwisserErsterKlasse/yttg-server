from typing import NotRequired, Required, TypedDict


class Proxy(TypedDict, total=True):
    """Telegram proxy config.

    >>> proxy: Proxy = Proxy(
    ...     scheme='http',
    ...     hostname='127.0.0.1',
    ...     port=1080,
    ... )
    """

    scheme: Required[str]
    hostname: Required[str]
    port: Required[int]
    username: NotRequired[str]
    password: NotRequired[str]
