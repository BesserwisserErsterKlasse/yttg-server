from asyncio import Event, wait_for
from contextlib import suppress
from dataclasses import dataclass
from getpass import getpass
from os import name as os_name
from pathlib import Path
from subprocess import run
from time import time
from typing import Any

from pyrogram.client import Client as PyrogramClient
from pyrogram.enums import ParseMode
from pyrogram.errors import BadRequest, SessionPasswordNeeded
from pyrogram.handlers.raw_update_handler import RawUpdateHandler
from pyrogram.raw.base.update import Update
from pyrogram.raw.functions.auth.export_login_token import ExportLoginToken
from pyrogram.raw.functions.auth.import_login_token import ImportLoginToken
from pyrogram.raw.functions.updates.get_state import GetState
from pyrogram.raw.types.auth.login_token import LoginToken
from pyrogram.raw.types.auth.login_token_migrate_to import LoginTokenMigrateTo
from pyrogram.raw.types.auth.login_token_success import LoginTokenSuccess
from pyrogram.raw.types.update_login_token import UpdateLoginToken

from modules.telegram.driver.const import (
    AUTH_HANDLER_GROUP,
    INCORRECT_PASSWORD_MESSAGE,
    QR_SCAN_HINT,
    TELEGRAM_2FA_PASSWORD_PROMPT,
)
from modules.telegram.driver.qr import show_telegram_login_qr
from modules.telegram.handler.temp import TempHandler
from modules.telegram.types import Proxy, TelegramDriverInitOptions

type AnyLoginToken = LoginToken | LoginTokenMigrateTo | LoginTokenSuccess


@dataclass(slots=True)
class TelegramDriver:
    __init_options: TelegramDriverInitOptions
    __client: PyrogramClient
    __login_event: Event

    def __init__(
        self,
        name: str,
        api_id: int,
        api_hash: str,
        app_version: str,
        lang_code: str,
        ipv6: bool,
        proxy: Proxy | None,
        workers: int,
        workdir: Path,
        parse_mode: ParseMode,
        sleep_threshold: int,
        hide_password: bool,
        max_concurrent_transmissions: int,
    ) -> None:
        self.__init_options = TelegramDriverInitOptions(
            name=name,
            api_id=api_id,
            api_hash=api_hash,
            app_version=app_version,
            lang_code=lang_code,
            ipv6=ipv6,
            proxy=proxy,  # type: ignore[typeddict-item]
            workers=workers,
            workdir=str(workdir),
            parse_mode=parse_mode,
            sleep_threshold=sleep_threshold,
            hide_password=hide_password,
            max_concurrent_transmissions=max_concurrent_transmissions,
        )
        self.__login_event = Event()

    async def start(self) -> None:
        """Start the Telegram client. Authorize via QR code if required."""

        self.__client = PyrogramClient(**self.__init_options)
        async with TempHandler(
            client=self.__client,
            handler=RawUpdateHandler(self.__on_update),
            group=AUTH_HANDLER_GROUP,
        ):
            is_authorized: bool = await self.__client.connect()
            await self.__client.initialize()
            if not is_authorized:
                try:
                    await self.__wait_for_scan()
                    await self.__finalize_login()
                except SessionPasswordNeeded:
                    await self.__check_password(max_attempts=3)
            await self.__client.invoke(GetState())

    @property
    def _client(self) -> PyrogramClient:
        return self.__client

    async def __on_update(
        self,
        client: PyrogramClient,
        update: Update,
        users: dict[int, Any],
        chats: dict[int, Any],
    ) -> None:
        del client, users, chats
        if isinstance(update, UpdateLoginToken):
            self.__login_event.set()

    async def __export[T1: AnyLoginToken, T2: AnyLoginToken](
        self, expected_types: tuple[type[T1], type[T2]]
    ) -> T1 | T2:
        assert self.__client.api_id is not None
        result: Any = await self.__client.invoke(
            ExportLoginToken(
                api_id=self.__client.api_id,
                api_hash=self.__client.api_hash,
                except_ids=[],
            )
        )
        assert isinstance(result, expected_types)
        return result

    async def __wait_for_scan(self) -> None:
        while True:
            token: LoginToken | LoginTokenSuccess = await self.__export(
                expected_types=(LoginToken, LoginTokenSuccess)
            )
            if isinstance(token, LoginTokenSuccess):
                break
            run(['cls' if os_name == 'nt' else 'clear'], shell=True)
            show_telegram_login_qr(token)
            print(QR_SCAN_HINT)
            with suppress(TimeoutError):
                await wait_for(
                    self.__login_event.wait(),
                    timeout=min(30, token.expires - int(time())),
                )
                break

    async def __finalize_login(self) -> None:
        login_result: LoginTokenMigrateTo | LoginTokenSuccess = await self.__export(
            expected_types=(LoginTokenMigrateTo, LoginTokenSuccess)
        )
        if isinstance(login_result, LoginTokenMigrateTo):
            await self.__client.session.dc_id_set(  # type: ignore[attr-defined]
                login_result.dc_id
            )
            login_result = await self.__client.invoke(
                ImportLoginToken(token=login_result.token)
            )
        if not isinstance(login_result, LoginTokenSuccess):
            raise RuntimeError(f'Login failed: {type(login_result)!r}')

    async def __check_password(self, max_attempts: int) -> None:
        for _ in range(max_attempts):
            try:
                password: str = getpass(f'{TELEGRAM_2FA_PASSWORD_PROMPT}: ')
                await self.__client.check_password(password)
                return None
            except BadRequest:
                print(INCORRECT_PASSWORD_MESSAGE)
        raise RuntimeError('Too many attempts!')
