from typing import Any, Required, TypedDict

from pyrogram.enums import ParseMode


class TelegramDriverInitOptions(TypedDict):
    name: Required[str]
    api_id: Required[int]
    api_hash: Required[str]
    app_version: Required[str]
    lang_code: Required[str]
    ipv6: Required[bool]
    proxy: Required[dict[Any, Any]]
    workers: Required[int]
    workdir: Required[str]
    parse_mode: Required[ParseMode]
    sleep_threshold: Required[int]
    hide_password: Required[bool]
    max_concurrent_transmissions: Required[int]
