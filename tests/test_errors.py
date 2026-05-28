# -*- coding: utf-8 -*-

import pytest
from v2kit import relabel, encode_subscription, decode_subscription
from v2kit import V2kitValidationError
from v2kit.validators import _validate_uri


INVALID_PROTOCOL = "http://example.com"

INVALID_VMESS = "vmess://invalid-base64"

VALID_VLESS = (
    "vless://1c4b4bca-e3ff-4ca8-a062-6f399ad3cf45@example.com:443"
    "?security=tls#test"
)


def test_validate_uri_non_string():
    with pytest.raises(V2kitValidationError):
        _validate_uri(123)


def test_validate_uri_empty():
    with pytest.raises(V2kitValidationError):
        _validate_uri("")


def test_validate_uri_missing_scheme():
    with pytest.raises(V2kitValidationError):
        _validate_uri("invalid-config")


def test_validate_uri_unsupported_protocol():
    with pytest.raises(V2kitValidationError):
        _validate_uri(INVALID_PROTOCOL)


def test_validate_invalid_vmess():
    with pytest.raises(V2kitValidationError):
        _validate_uri(INVALID_VMESS)


def test_relabel_invalid_config():
    with pytest.raises(V2kitValidationError):
        relabel("invalid", "label")


def test_relabel_empty_label():
    with pytest.raises(V2kitValidationError):
        relabel(VALID_VLESS, "")


def test_relabel_non_string_label():
    with pytest.raises(V2kitValidationError):
        relabel(VALID_VLESS, 123)


def test_encode_subscription_invalid_config():
    configs = [
        VALID_VLESS,
        "invalid-config",
    ]

    with pytest.raises(V2kitValidationError):
        encode_subscription(configs)


def test_decode_subscription_non_string():
    with pytest.raises(V2kitValidationError):
        decode_subscription(123)


def test_decode_subscription_invalid_data():
    with pytest.raises(Exception):
        decode_subscription("invalid-base64")


def test_decode_subscription_invalid_config():
    invalid_subscription = (
        "aW52YWxpZC1jb25maWc="
    )

    with pytest.raises(V2kitValidationError):
        decode_subscription(invalid_subscription)
