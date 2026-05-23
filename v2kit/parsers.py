# -*- coding: utf-8 -*-
"""v2kit parsers."""

from typing import Union
import json
from urllib.parse import urlparse, parse_qsl
from .params import Protocol
from .params import INVALID_URI_FORMAT_MESSAGE, UNSUPPORTED_PROTOCOL_MESSAGE
from .params import INVALID_VMESS_URI_MESSAGE, INVALID_SHADOWSOCKS_URI_MESSAGE
from .validators import _validate_non_empty_string
from .models import VMESSConfig, VLESSConfig, TrojanConfig, ShadowsocksConfig
from .utils import _decode_base64


def parse(uri: str) -> Union[VMESSConfig, VLESSConfig, TrojanConfig, ShadowsocksConfig]:
    """
    Parse V2Ray URI.

    :param uri: V2Ray URI.
    """
    _validate_non_empty_string(uri, "URI")

    if "://" not in uri:
        raise ValueError(INVALID_URI_FORMAT_MESSAGE)

    parsed = urlparse(uri)

    try:
        protocol = Protocol(
            parsed.scheme
        )

    except ValueError as exc:
        raise ValueError(UNSUPPORTED_PROTOCOL_MESSAGE.format(protocol=parsed.scheme)) from exc

    if protocol == Protocol.VMESS:
        return _parse_vmess(uri)

    if protocol == Protocol.VLESS:
        return _parse_vless(parsed)

    if protocol == Protocol.TROJAN:
        return _parse_trojan(parsed)

    if protocol == Protocol.SHADOWSOCKS:
        return _parse_shadowsocks(
            parsed
        )

    raise ValueError(UNSUPPORTED_PROTOCOL_MESSAGE.format(protocol=protocol))


def _parse_vmess(
    uri: str,
) -> VMESSConfig:
    """
    Parse VMESS URI.

    :param uri: VMESS URI.
    """
    KNOWN_VMESS_FIELDS = {
        "ps",
        "add",
        "port",
        "id",
        "aid",
        "net",
        "tls",
    }
    try:
        _, encoded = uri.split(
            "://",
            1,
        )

        decoded = _decode_base64(
            encoded
        )

        data = json.loads(decoded)

    except Exception as exc:
        raise ValueError(INVALID_VMESS_URI_MESSAGE) from exc

    extra = {
        key: value
        for key, value in data.items()
        if key not in KNOWN_VMESS_FIELDS
    }
    return VMESSConfig(
        uuid=data.get("id", ""),
        host=data.get("add", ""),
        port=int(
            data.get("port", 0)
        ),
        label=data.get("ps"),
        aid=int(
            data.get("aid", 0)
        ),
        network=data.get(
            "net",
            "tcp",
        ),
        tls=data.get(
            "tls",
            "",
        ),
        extra=extra,
    )


def _parse_vless(
    parsed,
) -> VLESSConfig:
    """
    Parse VLESS URI.

    :param parsed: Parsed URI object.
    """
    return VLESSConfig(
        uuid=parsed.username or "",
        host=parsed.hostname or "",
        port=parsed.port or 0,
        label=parsed.fragment or None,
        extra=dict(parse_qsl(parsed.query)),
    )


def _parse_trojan(
    parsed,
) -> TrojanConfig:
    """
    Parse Trojan URI.

    :param parsed: Parsed URI object.
    """
    return TrojanConfig(
        password=parsed.username or "",
        host=parsed.hostname or "",
        port=parsed.port or 0,
        label=parsed.fragment or None,
        extra=dict(parse_qsl(parsed.query)),
    )


def _parse_shadowsocks(
    parsed,
) -> ShadowsocksConfig:
    """
    Parse Shadowsocks URI.

    :param parsed: Parsed URI object.
    """
    try:
        userinfo = _decode_base64(
            parsed.username
        )

        encryption_method, password = (
            userinfo.split(
                ":",
                1,
            )
        )

    except Exception as exc:
        raise ValueError(INVALID_SHADOWSOCKS_URI_MESSAGE) from exc

    return ShadowsocksConfig(
        encryption_method=encryption_method,
        password=password,
        host=parsed.hostname or "",
        port=parsed.port or 0,
        label=parsed.fragment or None,
        extra=dict(parse_qsl(parsed.query)),
    )
