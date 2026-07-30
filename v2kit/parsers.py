# -*- coding: utf-8 -*-
"""v2kit parsers."""

from typing import Union
import json
from urllib.parse import urlparse, parse_qsl, unquote
from .errors import V2kitParseError
from .params import Protocol, SCHEME_TO_PROTOCOL
from .params import INVALID_URI_FORMAT_MESSAGE, UNSUPPORTED_PROTOCOL_MESSAGE
from .validators import _validate_non_empty_string
from .models import VMESSConfig, VLESSConfig, TrojanConfig, ShadowsocksConfig, SocksConfig, HttpConfig
from .utils import _decode_base64


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
        _, encoded = uri.split("://", 1)
        decoded = _decode_base64(encoded)
        data = json.loads(decoded)
        port = int(data.get("port", 0))
        alter_id = int(data.get("aid", 0))
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
        port=port,
        label=data.get("ps"),
        alter_id=alter_id,
        network=data.get("net", "tcp"),
        tls=data.get("tls", ""),
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
        label=unquote(parsed.fragment) or None,
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
        label=unquote(parsed.fragment) or None,
        extra=dict(parse_qsl(parsed.query)),
    )


def _parse_shadowsocks(uri: str) -> ShadowsocksConfig:
    """
    Parse Shadowsocks URI.

    :param uri: Shadowsocks URI.
    """
    parsed = urlparse(uri)
    try:
        userinfo = _decode_base64(parsed.username)
        encryption, password = (userinfo.split(":", 1))

    except Exception as exc:
        raise V2kitParseError(INVALID_URI_FORMAT_MESSAGE) from exc

    return ShadowsocksConfig(
        encryption=encryption,
        password=password,
        address=parsed.hostname or "",
        port=parsed.port or 0,
        label=unquote(parsed.fragment) or None,
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
        label=unquote(parsed.fragment) or None,
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
        label=unquote(parsed.fragment) or None,
        extra=dict(parse_qsl(parsed.query)),
    )


PARSERS = {
    Protocol.VMESS: _parse_vmess,
    Protocol.VLESS: _parse_vless,
    Protocol.TROJAN: _parse_trojan,
    Protocol.SHADOWSOCKS: _parse_shadowsocks,
    Protocol.SOCKS: _parse_socks,
    Protocol.HTTP: _parse_http,
}


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
        protocol = SCHEME_TO_PROTOCOL[parsed.scheme]
    except Exception as exc:
        raise V2kitParseError(UNSUPPORTED_PROTOCOL_MESSAGE.format(protocol=parsed.scheme)) from exc

    return PARSERS[protocol](uri)
