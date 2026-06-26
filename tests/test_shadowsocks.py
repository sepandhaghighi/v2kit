# -*- coding: utf-8 -*-
import pytest
from v2kit import parse
from v2kit import ShadowsocksConfig

def test_defaults():
    config = ShadowsocksConfig(
        encryption="aes-256-gcm",
        password="password",
        address="example.com",
        port=8388,
    )

    assert config.label is None
    assert config.extra == {}


def test_to_dict():
    config = ShadowsocksConfig(
        encryption="aes-256-gcm",
        password="password",
        address="example.com",
        port=8388,
        label="test",
        extra={"plugin": "v2ray-plugin"},
    )

    assert config.to_dict() == {
        "protocol": "shadowsocks",
        "encryption": "aes-256-gcm",
        "password": "password",
        "address": "example.com",
        "port": 8388,
        "label": "test",
        "extra": {"plugin": "v2ray-plugin"},
    }


def test_extra():
    config = ShadowsocksConfig(
        encryption="aes-256-gcm",
        password="password",
        address="example.com",
        port=8388,
        extra={"plugin": "v2ray-plugin"},
    )

    data = config.to_dict()

    assert data["extra"]["plugin"] == "v2ray-plugin"


def test_method_chaining():
    config = ShadowsocksConfig(
        encryption="aes-256-gcm",
        password="password",
        address="example.com",
        port=8388,
    )

    config.update_encryption(
        "chacha20-ietf-poly1305"
    ).update_password(
        "secret"
    ).update_address(
        "example.org"
    ).update_port(
        443
    )

    assert config.encryption == "chacha20-ietf-poly1305"
    assert config.password == "secret"
    assert config.address == "example.org"
    assert config.port == 443


@pytest.mark.parametrize(
    "kwargs",
    [
        {"encryption": ""},
        {"password": ""},
        {"address": ""},
        {"port": 0},
    ],
)
def test_invalid_values(kwargs):
    params = {
        "encryption": "aes-256-gcm",
        "password": "password",
        "address": "example.com",
        "port": 8388,
    }
    params.update(kwargs)

    with pytest.raises(ValueError):
        ShadowsocksConfig(**params)


def test_to_uri_roundtrip():
    config = ShadowsocksConfig(
        encryption="aes-256-gcm",
        password="password",
        address="example.com",
        port=8388,
        label="test",
    )

    parsed = parse(config.to_uri())

    assert parsed == config


def test_equality():
    config1 = ShadowsocksConfig(
        encryption="aes-256-gcm",
        password="password",
        address="example.com",
        port=8388,
    )

    config2 = ShadowsocksConfig(
        encryption="aes-256-gcm",
        password="password",
        address="example.com",
        port=8388,
    )

    config3 = ShadowsocksConfig(
        encryption="aes-256-gcm",
        password="password",
        address="example.org",
        port=8388,
    )

    assert config1 == config2
    assert config1 != config3


def test_repr():
    config = ShadowsocksConfig(
        encryption="aes-256-gcm",
        password="password",
        address="example.com",
        port=8388,
    )

    assert repr(config) == (
        "ShadowsocksConfig(protocol=<Protocol.SHADOWSOCKS: "
        "'shadowsocks'>, label=None)"
    )


def test_update_extra():
    config = ShadowsocksConfig(
        encryption="aes-256-gcm",
        password="password",
        address="example.com",
        port=8388,
    )

    config.update_extra(
        {"plugin": "v2ray-plugin"}
    )

    assert config.extra["plugin"] == "v2ray-plugin"


def test_update_methods():
    config = ShadowsocksConfig(
        encryption="aes-256-gcm",
        password="password",
        address="example.com",
        port=8388,
    )

    config.update_encryption(
        "chacha20-ietf-poly1305"
    )
    config.update_password(
        "secret"
    )
    config.update_address(
        "example.org"
    )
    config.update_port(
        443
    )

    assert config.encryption == "chacha20-ietf-poly1305"
    assert config.password == "secret"
    assert config.address == "example.org"
    assert config.port == 443
