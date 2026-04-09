from importlib.metadata import version

from pyrogram.enums import ParseMode

from env import env
from project.globalobjects.telegram.config import telegram_config
from project.telegram import YttgDriver

tg: YttgDriver = YttgDriver(
    name='yttg-server',
    api_id=env.telegram.api_id,
    api_hash=env.telegram.api_hash,
    app_version=f'yttg-{version('yttg-server')}',
    lang_code=telegram_config.language_code,
    ipv6=telegram_config.ipv6,
    proxy=telegram_config.proxy,
    workers=telegram_config.workers,
    workdir=telegram_config.workdir,
    parse_mode=ParseMode.DISABLED,
    sleep_threshold=telegram_config.sleep_threshold,
    hide_password=telegram_config.hide_password,
    max_concurrent_transmissions=telegram_config.max_concurrent_transmissions,
)
