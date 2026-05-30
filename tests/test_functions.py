# -*- coding: utf-8 -*-

import json
from v2kit import is_vmess, is_vless, is_trojan, is_shadowsocks, parse
from v2kit import relabel, encode_subscription, decode_subscription
from v2kit import VMESSConfig, VLESSConfig, TrojanConfig, ShadowsocksConfig
from v2kit.utils import _encode_base64


def create_vmess(label="test"):
    payload = {
        "v": "2",
        "ps": label,
        "add": "example.com",
        "port": "443",
        "id": "1c4b4bca-e3ff-4ca8-a062-6f399ad3cf45",
        "aid": "0",
        "net": "ws",
        "type": "none",
        "host": "",
        "path": "/",
        "tls": "tls",
    }
    encoded = _encode_base64(
        json.dumps(payload, ensure_ascii=False)
    )
    return f"vmess://{encoded}"


VMESS_CONFIG = create_vmess()

VLESS_CONFIG = (
    "vless://1c4b4bca-e3ff-4ca8-a062-6f399ad3cf45@example.com:443"
    "?security=tls#vless-test"
)

TROJAN_CONFIG = (
    "trojan://password@example.com:443"
    "?security=tls#trojan-test"
)

SHADOWSOCKS_CONFIG = (
    "ss://YWVzLTI1Ni1nY206cGFzc3dvcmQ=@example.com:8388#ss-test"
)


def test_is_vmess():
    assert is_vmess(VMESS_CONFIG) is True


def test_is_vless():
    assert is_vless(VLESS_CONFIG) is True


def test_is_trojan():
    assert is_trojan(TROJAN_CONFIG) is True


def test_is_shadowsocks():
    assert is_shadowsocks(SHADOWSOCKS_CONFIG) is True


def test_is_vmess_negative():
    assert is_vmess(VLESS_CONFIG) is False


def test_is_vmess_invalid():
    assert is_vmess("invalid") is False


def test_is_vless_invalid():
    assert is_vless("invalid") is False


def test_is_trojan_invalid():
    assert is_trojan("invalid") is False


def test_is_shadowsocks_invalid():
    assert is_shadowsocks("invalid") is False


def test_relabel_vmess():
    result = relabel(VMESS_CONFIG, "new-label")

    assert is_vmess(result) is True

    encoded = result.split("://", 1)[1]
    decoded = json.loads(
        __import__("base64").b64decode(encoded + "==").decode()
    )

    assert decoded["ps"] == "new-label"


def test_relabel_vless():
    result = relabel(VLESS_CONFIG, "new-label")

    assert result.endswith("#new-label")


def test_relabel_trojan():
    result = relabel(TROJAN_CONFIG, "new-label")

    assert result.endswith("#new-label")


def test_relabel_shadowsocks():
    result = relabel(SHADOWSOCKS_CONFIG, "new-label")

    assert result.endswith("#new-label")


def test_encode_subscription():
    configs = [
        VMESS_CONFIG,
        VLESS_CONFIG,
    ]

    result = encode_subscription(configs)

    assert isinstance(result, str)
    assert len(result) > 0


def test_decode_subscription():
    configs = [
        VMESS_CONFIG,
        VLESS_CONFIG,
    ]

    encoded = encode_subscription(configs)

    result = decode_subscription(encoded)

    assert result == configs


def test_encode_decode_subscription_roundtrip():
    configs = [
        VMESS_CONFIG,
        VLESS_CONFIG,
        TROJAN_CONFIG,
        SHADOWSOCKS_CONFIG,
    ]

    encoded = encode_subscription(configs)
    decoded = decode_subscription(encoded)

    assert decoded == configs


def test_encode_subscription_with_models():
    config = parse(VLESS_CONFIG)

    result = encode_subscription([config])

    assert isinstance(result, str)


def test_encode_subscription_no_validation():
    result = encode_subscription(
        ["invalid-config"],
        validate=False,
    )

    assert isinstance(result, str)


def test_decode_subscription_no_validation():
    encoded = _encode_base64(
        "invalid-config"
    )

    result = decode_subscription(
        encoded,
        validate=False,
    )

    assert result == ["invalid-config"]


def test_parse_vmess():
    assert isinstance(
        parse(VMESS_CONFIG),
        VMESSConfig,
    )


def test_parse_vless():
    assert isinstance(
        parse(VLESS_CONFIG),
        VLESSConfig,
    )


def test_parse_trojan():
    assert isinstance(
        parse(TROJAN_CONFIG),
        TrojanConfig,
    )


def test_parse_shadowsocks():
    assert isinstance(
        parse(SHADOWSOCKS_CONFIG),
        ShadowsocksConfig,
    )
