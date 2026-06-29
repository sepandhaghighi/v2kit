# -*- coding: utf-8 -*-
"""v2kit parsers."""

from typing import Union
import json
from urllib.parse import urlparse, parse_qsl
from .errors import V2kitParseError
from .params import Protocol
from .params import INVALID_URI_FORMAT_MESSAGE, UNSUPPORTED_PROTOCOL_MESSAGE
from .validators import _validate_non_empty_string
from .models import VMESSConfig, VLESSConfig, TrojanConfig, ShadowsocksConfig, SocksConfig, HttpConfig
from .utils import _decode_base64


def parse(uri: str) -> Union[VMESSConfig, VLESSConfig, TrojanConfig, ShadowsocksConfig, SocksConfig, HttpConfig]:
    """
    Parse V2Ray URI.

    :param uri: V2Ray URI.
    """
    _validate_non_empty_string(uri, "URI")

    if "://" not in uri:
        raise V2kitParseError(INVALID_URI_FORMAT_MESSAGE)

    parsed = urlparse(uri)

    try:
        protocol = Protocol(
            parsed.scheme
        )

    except Exception as exc:
        raise V2kitParseError(UNSUPPORTED_PROTOCOL_MESSAGE.format(protocol=parsed.scheme)) from exc

    if protocol == Protocol.VMESS:
        return _parse_vmess(uri)

    if protocol == Protocol.VLESS:
        return _parse_vless(uri)

    if protocol == Protocol.TROJAN:
        return _parse_trojan(uri)

    if protocol == Protocol.SHADOWSOCKS:
        return _parse_shadowsocks(uri)

    if protocol == Protocol.SOCKS:
        return _parse_socks(uri)
    if protocol == Protocol.HTTP:
        return _parse_http(uri)


def _parse_vmess(uri: str) -> VMESSConfig:
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
        raise V2kitParseError(INVALID_URI_FORMAT_MESSAGE) from exc

    extra = {
        key: value
        for key, value in data.items()
        if key not in KNOWN_VMESS_FIELDS
    }
    return VMESSConfig(
        uuid=data.get("id", ""),
        address=data.get("add", ""),
        port=int(
            data.get("port", 0)
        ),
        label=data.get("ps"),
        alter_id=int(
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


def _parse_vless(uri: str) -> VLESSConfig:
    """
    Parse VLESS URI.

    :param uri: VLESS URI.
    """
    parsed = urlparse(uri)
    return VLESSConfig(
        uuid=parsed.username or "",
        address=parsed.hostname or "",
        port=parsed.port or 0,
        label=parsed.fragment or None,
        extra=dict(parse_qsl(parsed.query)),
    )


def _parse_trojan(uri: str) -> TrojanConfig:
    """
    Parse Trojan URI.

    :param uri: Trojan URI.
    """
    parsed = urlparse(uri)
    return TrojanConfig(
        password=parsed.username or "",
        address=parsed.hostname or "",
        port=parsed.port or 0,
        label=parsed.fragment or None,
        extra=dict(parse_qsl(parsed.query)),
    )


def _parse_shadowsocks(uri: str) -> ShadowsocksConfig:
    """
    Parse Shadowsocks URI.

    :param uri: Shadowsocks URI.
    """
    parsed = urlparse(uri)
    try:
        userinfo = _decode_base64(
            parsed.username
        )

        encryption, password = (
            userinfo.split(
                ":",
                1,
            )
        )

    except Exception as exc:
        raise V2kitParseError(INVALID_URI_FORMAT_MESSAGE) from exc

    return ShadowsocksConfig(
        encryption=encryption,
        password=password,
        address=parsed.hostname or "",
        port=parsed.port or 0,
        label=parsed.fragment or None,
        extra=dict(parse_qsl(parsed.query)),
    )


def _parse_socks(uri: str) -> SocksConfig:
    """
    Parse SOCKS URI.

    :param uri: SOCKS URI.
    """
    parsed = urlparse(uri)

    return SocksConfig(
        address=parsed.hostname or "",
        port=parsed.port or 0,
        username=parsed.username or None,
        password=parsed.password or None,
        label=parsed.fragment or None,
        extra=dict(parse_qsl(parsed.query)),
    )


def _parse_http(uri: str) -> HttpConfig:
    """
    Parse HTTP URI.

    :param uri: HTTP URI.
    """
    parsed = urlparse(uri)

    return HttpConfig(
        address=parsed.hostname or "",
        port=parsed.port or 0,
        username=parsed.username or None,
        password=parsed.password or None,
        label=parsed.fragment or None,
        extra=dict(parse_qsl(parsed.query)),
    )
