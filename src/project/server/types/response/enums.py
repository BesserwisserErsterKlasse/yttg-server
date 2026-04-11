from enum import IntEnum, StrEnum


class ResponseStatus(IntEnum):
    SUCCESS = 0
    TELEGRAM_ERROR = 1
    INTERNAL_ERROR = 2
    CLIENT_ERROR = 3


class YttgErrorMessage(StrEnum):
    UNMATCHED_REQUEST = 'Request was not matched'
    ILL_FORMED_LINK = 'Invalid link has been passed'
    INVALID_CHANNEL_HASH = 'Invalid channel hash'
    NO_RESULT_FOUND = 'Video is not available or does not exist'
    NOT_SUBSCRIBED_ERROR = (
        'Telegram user not subscribed to channels required by the provider'
    )
