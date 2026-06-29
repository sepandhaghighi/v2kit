# -*- coding: utf-8 -*-

import pytest
from v2kit import VMESSConfig, VLESSConfig, TrojanConfig, ShadowsocksConfig, SocksConfig
from v2kit import relabel, encode_subscription, decode_subscription, parse
from v2kit import V2kitError, V2kitValidationError, V2kitParseError
from v2kit.validators import _validate_uri


INVALID_PROTOCOL = "ftp://example.com"

INVALID_VMESS = "vmess://invalid-base64"

INVALID_SHADOWSOCKS = "ss://invalid-base64@example.com:8388#ss-test"

VALID_VLESS = (
    "vless://1c4b4bca-e3ff-4ca8-a062-6f399ad3cf45@example.com:443"
    "?security=tls#test"
)

VALID_UUID = (
    "1c4b4bca-e3ff-4ca8-a062-6f399ad3cf45"
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


def test_exception_hierarchy():
    assert issubclass(
        V2kitValidationError,
        V2kitError,
    )

    assert issubclass(
        V2kitParseError,
        V2kitValidationError,
    )


def test_parse_invalid_uri():
    with pytest.raises(V2kitParseError):
        parse("invalid")


def test_parse_unsupported_protocol():
    with pytest.raises(V2kitParseError):
        parse(INVALID_PROTOCOL)


def test_parse_invalid_vmess():
    with pytest.raises(V2kitParseError):
        parse(INVALID_VMESS)


def test_parse_invalid_shadowsocks():
    with pytest.raises(V2kitParseError):
        parse(INVALID_SHADOWSOCKS)


def test_vless_invalid_uuid():
    with pytest.raises(V2kitValidationError):
        VLESSConfig(
            uuid="invalid",
            address="example.com",
            port=443,
        )


def test_vless_invalid_port():
    with pytest.raises(V2kitValidationError):
        VLESSConfig(
            uuid=VALID_UUID,
            address="example.com",
            port=70000,
        )


def test_vless_empty_address():
    with pytest.raises(V2kitValidationError):
        VLESSConfig(
            uuid=VALID_UUID,
            address="",
            port=443,
        )


def test_vmess_invalid_alter_id():
    with pytest.raises(V2kitValidationError):
        VMESSConfig(
            uuid=VALID_UUID,
            address="example.com",
            port=443,
            alter_id=-1,
        )


def test_trojan_empty_password():
    with pytest.raises(V2kitValidationError):
        TrojanConfig(
            password="",
            address="example.com",
            port=443,
        )


def test_shadowsocks_empty_encryption():
    with pytest.raises(V2kitValidationError):
        ShadowsocksConfig(
            encryption="",
            password="secret",
            address="example.com",
            port=8388,
        )


def test_socks_invalid_port():
    with pytest.raises(V2kitValidationError):
        SocksConfig(
            address="example.com",
            port=70000,
        )


def test_socks_empty_address():
    with pytest.raises(V2kitValidationError):
        SocksConfig(
            address="",
            port=1080,
        )


def test_socks_invalid_username():
    with pytest.raises(V2kitValidationError):
        SocksConfig(
            address="example.com",
            port=1080,
            username="",
        )


def test_socks_invalid_password():
    with pytest.raises(V2kitValidationError):
        SocksConfig(
            address="example.com",
            port=1080,
            password="",
        )
