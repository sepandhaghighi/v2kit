# -*- coding: utf-8 -*-

import pytest

from v2kit import relabel, encode_subscription, decode_subscription
from v2kit.utils import _validate_config


INVALID_PROTOCOL = "http://example.com"

INVALID_VMESS = "vmess://invalid-base64"

VALID_VLESS = (
    "vless://uuid@example.com:443"
    "?security=tls#test"
)


def test_validate_config_non_string():
    with pytest.raises(TypeError):
        _validate_config(123)


def test_validate_config_empty():
    with pytest.raises(ValueError):
        _validate_config("")


def test_validate_config_missing_scheme():
    with pytest.raises(ValueError):
        _validate_config("invalid-config")


def test_validate_config_unsupported_protocol():
    with pytest.raises(ValueError):
        _validate_config(INVALID_PROTOCOL)


def test_validate_invalid_vmess():
    with pytest.raises(ValueError):
        _validate_config(INVALID_VMESS)


def test_relabel_invalid_config():
    with pytest.raises(ValueError):
        relabel("invalid", "label")


def test_relabel_empty_label():
    with pytest.raises(ValueError):
        relabel(VALID_VLESS, "")


def test_relabel_non_string_label():
    with pytest.raises(TypeError):
        relabel(VALID_VLESS, 123)


def test_encode_subscription_invalid_config():
    configs = [
        VALID_VLESS,
        "invalid-config",
    ]

    with pytest.raises(ValueError):
        encode_subscription(configs)


def test_decode_subscription_non_string():
    with pytest.raises(TypeError):
        decode_subscription(123)


def test_decode_subscription_invalid_data():
    with pytest.raises(Exception):
        decode_subscription("invalid-base64")


def test_decode_subscription_invalid_config():
    invalid_subscription = (
        "aW52YWxpZC1jb25maWc="
    )

    with pytest.raises(ValueError):
        decode_subscription(invalid_subscription)