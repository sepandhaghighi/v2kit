# -*- coding: utf-8 -*-
from v2kit import parse
from v2kit import VMESSConfig, VLESSConfig
from v2kit import TrojanConfig, ShadowsocksConfig

def test_vmess_to_uri_roundtrip():
    config = VMESSConfig(
        uuid="1c4b4bca-e3ff-4ca8-a062-6f399ad3cf45",
        address="example.com",
        port=443,
        label="test",
    )

    parsed = parse(config.to_uri())

    assert parsed == config


def test_vmess_update_methods():
    config = VMESSConfig(
        uuid="1c4b4bca-e3ff-4ca8-a062-6f399ad3cf45",
        address="example.com",
        port=443,
    )

    config.update_network("ws")
    config.update_tls("tls")
    config.update_alter_id(1)

    assert config.network == "ws"
    assert config.tls == "tls"
    assert config.alter_id == 1


def test_vless_to_uri_roundtrip():
    config = VLESSConfig(
        uuid="1c4b4bca-e3ff-4ca8-a062-6f399ad3cf45",
        address="example.com",
        port=443,
        label="test",
        extra={"security": "tls"},
    )

    parsed = parse(config.to_uri())

    assert parsed == config

def test_trojan_to_uri_roundtrip():
    config = TrojanConfig(
        password="password",
        address="example.com",
        port=443,
        label="test",
    )

    parsed = parse(config.to_uri())

    assert parsed == config


def test_shadowsocks_to_uri_roundtrip():
    config = ShadowsocksConfig(
        encryption="aes-256-gcm",
        password="password",
        address="example.com",
        port=8388,
        label="test",
    )

    parsed = parse(config.to_uri())

    assert parsed == config


def test_config_equality():
    config1 = VLESSConfig(
        uuid="1c4b4bca-e3ff-4ca8-a062-6f399ad3cf45",
        address="example.com",
        port=443,
    )

    config2 = VLESSConfig(
        uuid="1c4b4bca-e3ff-4ca8-a062-6f399ad3cf45",
        address="example.com",
        port=443,
    )

    assert config1 == config2


def test_config_repr():
    config = VLESSConfig(
        uuid="1c4b4bca-e3ff-4ca8-a062-6f399ad3cf45",
        address="example.com",
        port=443,
    )

    assert "VLESSConfig" in repr(config)


def test_update_extra():
    config = VLESSConfig(
        uuid="1c4b4bca-e3ff-4ca8-a062-6f399ad3cf45",
        address="example.com",
        port=443,
    )

    config.update_extra(
        {"security": "tls"}
    )

    assert config.extra["security"] == "tls"