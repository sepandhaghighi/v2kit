# -*- coding: utf-8 -*-
"""v2kit utils."""
import json
import base64
from typing import Iterable
from urllib.parse import urlparse
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


def _validate_config(config: str) -> None:
    """
    Validate V2Ray config format.

    :param config: V2Ray config.
    """
    if not isinstance(config, str):
        raise TypeError("Config must be str.")

    if len(config) == 0:
        raise ValueError("Config cannot be empty.")

    if "://" not in config:
        raise ValueError("Invalid config format.")

    parsed = urlparse(config)

    try:
        Protocol(parsed.scheme)
    except ValueError as exc:
        raise ValueError(
            f"Unsupported protocol: {parsed.scheme}"
        ) from exc

    if parsed.scheme == Protocol.VMESS.value:
        try:
            _, encoded = config.split("://", 1)

            encoded = _add_base64_padding(encoded)

            decoded = _decode_base64(encoded)

            data = json.loads(decoded)

            if not isinstance(data, dict):
                raise ValueError

        except Exception as exc:
            raise ValueError(
                "Invalid VMESS config."
            ) from exc


def _validate_label(label: str) -> None:
    """
    Validate config label.

    :param label: Config label.
    """
    if not isinstance(label, str):
        raise TypeError("Label must be str.")

    if len(label) == 0:
        raise ValueError("Label cannot be empty.")


def _get_protocol(config: str) -> Protocol:
    """
    Extract protocol from config.

    :param config: V2Ray config.
    """
    _validate_config(config)

    protocol = config.split("://", 1)[0]

    return Protocol(protocol)


def _relabel_vmess(config: str, label: str) -> str:
    """
    Relabel VMESS config.

    :param config: VMESS config.
    :param label: New label.
    """
    _validate_config(config)
    _validate_label(label)

    protocol, encoded = config.split("://", 1)

    decoded = _decode_base64(encoded)

    data = json.loads(decoded)

    data["ps"] = label

    encoded_new = _encode_base64(
        json.dumps(data, ensure_ascii=False)
    )

    return f"{protocol}://{encoded_new}"


def _relabel_tag(config: str, label: str) -> str:
    """
    Relabel VLESS, Trojan and Shadowsocks configs.

    :param config: Input config.
    :param label: New label.
    """
    _validate_config(config)
    _validate_label(label)
    base = config.split("#", 1)[0]

    return f"{base}#{label}"


def _is_protocol(config: str, protocol: Protocol) -> bool:
    """
    Check whether config uses given protocol.

    :param config: V2Ray config.
    :param protocol: Target protocol.
    """
    try:
        return _get_protocol(config) == protocol
    except Exception:
        return False
