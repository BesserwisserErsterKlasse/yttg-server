from enum import StrEnum


class ResponseStatus(StrEnum):
    SUCCESS = 'success'
    CLIENT_ERROR = 'client-error'
    INTERNAL_ERROR = 'internal-error'
    TELEGRAM_ERROR = 'telegram-error'


class YttgErrorMessage(StrEnum):
    UNMATCHED_REQUEST = 'Request was not matched'
    ILL_FORMED_LINK = 'Invalid link has been passed'
    INVALID_CHANNEL_HASH = 'Invalid channel hash'
    INVALID_LANGUAGE = 'Invalid language'
    NO_RESULT_FOUND = 'Video is not available or does not exist'
    NOT_SUBSCRIBED_ERROR = (
        'Telegram user not subscribed to channels required by the provider'
    )
