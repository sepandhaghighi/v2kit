# -*- coding: utf-8 -*-
"""v2kit utils."""
import json
import base64
from typing import Iterable
from urllib.parse import urlparse
from .errors import V2kitValidationError, V2kitParseError
from .validators import _validate_label
from .params import DEFAULT_ENCODING
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


def _validate_config(uri: str) -> None:
    """
    Validate V2Ray URI format.

    :param uri: V2Ray URI.
    """
    if not isinstance(uri, str):
        raise V2kitValidationError("Config must be str.")

    if len(uri) == 0:
        raise V2kitValidationError("Config cannot be empty.")

    if "://" not in uri:
        raise V2kitParseError("Invalid config format.")

    parsed = urlparse(uri)

    try:
        Protocol(parsed.scheme)
    except Exception as exc:
        raise V2kitParseError(
            f"Unsupported protocol: {parsed.scheme}"
        ) from exc

    if parsed.scheme == Protocol.VMESS.value:
        try:
            _, encoded = uri.split("://", 1)

            encoded = _add_base64_padding(encoded)

            decoded = _decode_base64(encoded)

            data = json.loads(decoded)

            if not isinstance(data, dict):
                raise ValueError

        except Exception as exc:
            raise V2kitParseError(
                "Invalid VMESS config."
            ) from exc


def _get_protocol(uri: str) -> Protocol:
    """
    Extract protocol from URI.

    :param uri: V2Ray URI.
    """
    _validate_config(uri)

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
