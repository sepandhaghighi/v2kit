# -*- coding: utf-8 -*-
"""v2kit functions."""
from typing import Iterable
from .params import Protocol
from .utils import _get_protocol, _is_protocol
from .utils import _relabel_vmess, _relabel_tag
from .utils import _encode_base64, _decode_base64
from .utils import _validate_config

def is_vmess(config: str) -> bool:
    """
    Check whether config is VMESS.

    :param config: V2Ray config.
    """
    return _is_protocol(config, Protocol.VMESS)


def is_vless(config: str) -> bool:
    """
    Check whether config is VLESS.

    :param config: V2Ray config.
    """
    return _is_protocol(config, Protocol.VLESS)


def is_trojan(config: str) -> bool:
    """
    Check whether config is Trojan.

    :param config: V2Ray config.
    """
    return _is_protocol(config, Protocol.TROJAN)


def is_shadowsocks(config: str) -> bool:
    """
    Check whether config is Shadowsocks.

    :param config: V2Ray config.
    """
    return _is_protocol(config, Protocol.SHADOWSOCKS)


def relabel(config: str, label: str) -> str:
    """
    Relabel any supported config.

    :type config: str
    :type label: str
    """
    protocol = _get_protocol(config)

    if protocol == Protocol.VMESS:
        return _relabel_vmess(config, label)

    return _relabel_tag(config, label)


def encode_subscription(
    configs: Iterable[str],
    validate: bool = True,
) -> str:
    """
    Encode configs as V2Ray subscription.

    :param configs: Iterable of configs.
    :param validate: Validate configs before encoding.
    """
    config_list = list(configs)

    if validate:
        for config in config_list:
            _validate_config(config)

    subscription = "\n".join(config_list)

    return _encode_base64(subscription)


def decode_subscription(
    subscription: str,
    validate: bool = True,
) -> list[str]:
    """
    Decode V2Ray subscription.

    :param subscription: Base64 subscription.
    :param validate: Validate decoded configs.
    """
    if not isinstance(subscription, str):
        raise TypeError(
            "Subscription must be str."
        )

    decoded = _decode_base64(subscription)

    configs = decoded.splitlines()

    if validate:
        for config in configs:
            _validate_config(config)

    return configs
