# -*- coding: utf-8 -*-
"""v2kit functions."""
from typing import Iterable, List
from .params import Protocol
from .utils import _get_protocol, _is_protocol
from .utils import _relabel_vmess, _relabel_tag
from .utils import _encode_base64, _decode_base64
from .utils import _validate_config


def is_vmess(uri: str) -> bool:
    """
    Check whether URI is VMESS.

    :param uri: V2Ray URI.
    """
    return _is_protocol(uri, Protocol.VMESS)


def is_vless(uri: str) -> bool:
    """
    Check whether URI is VLESS.

    :param uri: V2Ray URI.
    """
    return _is_protocol(uri, Protocol.VLESS)


def is_trojan(uri: str) -> bool:
    """
    Check whether URI is Trojan.

    :param uri: V2Ray URI.
    """
    return _is_protocol(uri, Protocol.TROJAN)


def is_shadowsocks(uri: str) -> bool:
    """
    Check whether URI is Shadowsocks.

    :param uri: V2Ray URI.
    """
    return _is_protocol(uri, Protocol.SHADOWSOCKS)


def relabel(uri: str, label: str) -> str:
    """
    Relabel any supported URI.

    :param uri: V2Ray URI.
    :param label: New label.
    """
    protocol = _get_protocol(uri)

    if protocol == Protocol.VMESS:
        return _relabel_vmess(uri, label)

    return _relabel_tag(uri, label)


def encode_subscription(
    entries: Iterable[str],
    validate: bool = True,
) -> str:
    """
    Encode entries as V2Ray subscription.

    :param entries: Iterable of entries.
    :param validate: Validate entries before encoding.
    """
    uri_list = list(entries)

    if validate:
        for uri in uri_list:
            _validate_config(uri)

    subscription = "\n".join(uri_list)

    return _encode_base64(subscription)


def decode_subscription(
    subscription: str,
    validate: bool = True,
) -> List[str]:
    """
    Decode V2Ray subscription.

    :param subscription: Base64 subscription.
    :param validate: Validate decoded URI list.
    """
    if not isinstance(subscription, str):
        raise TypeError(
            "Subscription must be str."
        )

    decoded = _decode_base64(subscription)

    uri_list = decoded.splitlines()

    if validate:
        for uri in uri_list:
            _validate_config(uri)

    return uri_list
