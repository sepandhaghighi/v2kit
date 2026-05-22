# -*- coding: utf-8 -*-
"""v2kit parsers."""

from typing import Union
import json
from urllib.parse import urlparse, parse_qsl
from .params import Protocol
from .models import VMESSConfig, VLESSConfig, TrojanConfig, ShadowsocksConfig
from .utils import _decode_base64


def parse(uri: str) -> Union[VMESSConfig, VLESSConfig, TrojanConfig, ShadowsocksConfig]:
    """
    Parse V2Ray URI.

    :param uri: V2Ray URI.
    """
    if not isinstance(uri, str):
        raise TypeError("URI must be str.")

    if len(uri.strip()) == 0:
        raise ValueError("URI cannot be empty.")

    if "://" not in uri:
        raise ValueError("Invalid URI format.")

    parsed = urlparse(uri)

    try:
        protocol = Protocol(
            parsed.scheme
        )

    except ValueError as exc:
        raise ValueError(
            f"Unsupported protocol: "
            f"{parsed.scheme}"
        ) from exc

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

    raise ValueError(
        f"Unsupported protocol: "
        f"{protocol}"
    )


def _parse_vmess(
    uri: str,
) -> VMESSConfig:
    """
    Parse VMESS URI.

    :param uri: VMESS URI.
    """
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
        raise ValueError("Invalid VMESS URI.") from exc

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
        extra=data,
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
        raise ValueError("Invalid Shadowsocks URI.") from exc

    return ShadowsocksConfig(
        encryption_method=encryption_method,
        password=password,
        host=parsed.hostname or "",
        port=parsed.port or 0,
        label=parsed.fragment or None,
        extra=dict(parse_qsl(parsed.query)),
    )
