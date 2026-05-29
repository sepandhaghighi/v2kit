# -*- coding: utf-8 -*-
"""v2kit utils."""
import base64
from typing import Iterable
from .errors import V2kitValidationError, V2kitParseError
from .validators import _validate_non_empty_string, _validate_uri
from .params import DEFAULT_ENCODING, INVALID_URI_FORMAT_MESSAGE
from .params import Protocol


def _encode_base64(data: str) -> str:
    """
    Encode string to base64.

    :param data: Input string.
    """
    return base64.b64encode(
        data.encode(DEFAULT_ENCODING)
    ).decode(DEFAULT_ENCODING)


def _decode_base64(data: str) -> str:
    """
    Decode base64 string.

    :param data: Base64 encoded string.
    """
    padded = _add_base64_padding(data)

    return base64.b64decode(
        padded
    ).decode(DEFAULT_ENCODING)


def _add_base64_padding(data: str) -> str:
    """
    Add missing base64 padding.

    :param data: Base64 string.
    """
    return data + "=" * (-len(data) % 4)


def _get_protocol(uri: str) -> Protocol:
    """
    Extract protocol from URI.

    :param uri: V2Ray URI.
    """
    _validate_uri(uri)

    protocol = uri.split("://", 1)[0]

    return Protocol(protocol)


def _is_protocol(uri: str, protocol: Protocol) -> bool:
    """
    Check whether URI uses given protocol.

    :param uri: V2Ray URI.
    :param protocol: Target protocol.
    """
    try:
        return _get_protocol(uri) == protocol
    except Exception:
        return False
