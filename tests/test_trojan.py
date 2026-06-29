# -*- coding: utf-8 -*-

import pytest
from v2kit import parse
from v2kit import TrojanConfig


def test_defaults():
    config = TrojanConfig(
        password="password",
        address="example.com",
        port=443,
    )

    assert config.label is None
    assert config.extra == {}


def test_to_dict():
    config = TrojanConfig(
        password="password",
        address="example.com",
        port=443,
        label="test",
        extra={"security": "tls"},
    )

    assert config.to_dict() == {
        "protocol": "trojan",
        "password": "password",
        "address": "example.com",
        "port": 443,
        "extra": {"security": "tls"},
        "label": "test",
    }


def test_extra():
    config = TrojanConfig(
        password="password",
        address="example.com",
        port=443,
        extra={"security": "tls"},
    )

    data = config.to_dict()

    assert data["extra"]["security"] == "tls"


def test_method_chaining():
    config = TrojanConfig(
        password="password",
        address="example.com",
        port=443,
    )

    config.update_password("new-password").update_address("example.org").update_port(8443)

    assert config.password == "new-password"
    assert config.address == "example.org"
    assert config.port == 8443


@pytest.mark.parametrize(
    "kwargs",
    [
        {"password": ""},
        {"address": ""},
        {"port": 0},
        {"port": 1.2},
        {"extra": 1},
    ],
)
def test_invalid_values(kwargs):
    params = {
        "password": "password",
        "address": "example.com",
        "port": 443,
    }
    params.update(kwargs)

    with pytest.raises(ValueError):
        TrojanConfig(**params)


def test_equality():
    config1 = TrojanConfig(
        password="password",
        address="example.com",
        port=443,
    )

    config2 = TrojanConfig(
        password="password",
        address="example.com",
        port=443,
    )

    config3 = TrojanConfig(
        password="password",
        address="example.org",
        port=443,
    )

    assert config1 == config2
    assert config1 != config3
    assert config1 != "config1"


def test_repr():
    config = TrojanConfig(
        password="password",
        address="example.com",
        port=443,
    )

    assert repr(config) == "TrojanConfig(protocol=<Protocol.TROJAN: 'trojan'>, label=None)"


def test_to_uri_roundtrip():
    config = TrojanConfig(
        password="password",
        address="example.com",
        port=443,
        label="test",
    )

    parsed = parse(config.to_uri())

    assert parsed == config


def test_update_extra():
    config = TrojanConfig(
        password="password",
        address="example.com",
        port=443,
    )

    config.update_extra(
        {"security": "tls"}
    )

    assert config.extra["security"] == "tls"


def test_update_methods():
    config = TrojanConfig(
        password="password",
        address="example.com",
        port=443,
    )

    config.update_password("new-password")
    config.update_address("example.org")
    config.update_port(8443)

    assert config.password == "new-password"
    assert config.address == "example.org"
    assert config.port == 8443
