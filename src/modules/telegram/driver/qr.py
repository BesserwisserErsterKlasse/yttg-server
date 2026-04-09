from base64 import urlsafe_b64encode

from pyrogram.raw.types.auth.login_token import LoginToken
from qrcode import ERROR_CORRECT_H, QRCode  # type: ignore[import-untyped]


def show_telegram_login_qr(token: LoginToken) -> None:
    """Print an ASCII Telegram login QR code to a console."""

    encoded_token: str = urlsafe_b64encode(token.token).decode('ascii').rstrip('=')
    url: str = f'tg://login?token={encoded_token}'
    qr: QRCode = QRCode(error_correction=ERROR_CORRECT_H, border=1)
    qr.add_data(url)
    qr.make(fit=True)
    qr.print_ascii(invert=True)
