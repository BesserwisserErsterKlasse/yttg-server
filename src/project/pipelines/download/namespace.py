from enum import StrEnum


class OnStreamSelectionResponse(StrEnum):
    MEDIA_MESSAGE = 'download-media-message'
    NOT_SUBSCRIBED_ERROR = 'not-subscribed-error'
