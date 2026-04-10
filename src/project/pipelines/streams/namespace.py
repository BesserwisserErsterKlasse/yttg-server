from enum import StrEnum


class OnLinkResponse(StrEnum):
    STREAMS = 'streams-message'
    ILL_FORMED_LINK_ERROR = 'ill-formed-link-error'
    NO_RESULTS_FOUND_ERROR = 'no-result-error'
