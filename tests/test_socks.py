# -*- coding: utf-8 -*-
import pytest
from v2kit import V2kitValidationError
from v2kit import parse
from v2kit import SocksConfig


def test_defaults():
    config = SocksConfig(
        address="example.com",
        port=1080,
    )

    assert config.label is None
    assert config.extra == {}


def test_to_dict():
    config = SocksConfig(
        address="example.com",
        port=1080,
        username="user",
        password="password",
        label="test",
        extra={"version": "5"},
    )

    assert config.to_dict() == {
        "protocol": "socks",
        "address": "example.com",
        "port": 1080,
        "username": "user",
        "password": "password",
        "label": "test",
        "extra": {"version": "5"},
    }


def test_extra():
    config = SocksConfig(
        address="example.com",
        port=1080,
        extra={"version": "5"},
    )

    data = config.to_dict()

    assert data["extra"]["version"] == "5"


def test_method_chaining():
    config = SocksConfig(
        address="example.com",
        port=1080,
    )

    config.update_address(
        "example.org"
    ).update_port(
        2080
    ).update_username(
        "user"
    ).update_password(
        "password"
    ).set_extra_item(
        "version",
        "5",
    ).remove_extra_item(
        "version"
    ).clear_extra()

    assert config.address == "example.org"
    assert config.port == 2080
    assert config.username == "user"
    assert config.password == "password"
    assert config.extra == {}


@pytest.mark.parametrize(
    "kwargs, expected_message",
    [
        ({"address": ""}, r"Address cannot be empty."),
        ({"port": 0}, r"Invalid port: 0"),
        ({"port": 1.2}, r"Port must be int."),
        ({"username": ""}, r"Username cannot be empty."),
        ({"password": ""}, r"Password cannot be empty."),
        ({"extra": 1}, r"Extra must be dict."),
    ],
)
def test_invalid_values(kwargs, expected_message):
    params = {
        "address": "example.com",
        "port": 1080,
    }
    params.update(kwargs)

    with pytest.raises(V2kitValidationError, match=expected_message):
        SocksConfig(**params)


def test_update_methods():
    config = SocksConfig(
        address="example.com",
        port=1080,
    )

    config.update_address("example.org")
    config.update_port(2080)
    config.update_username("user")
    config.update_password("password")

    assert config.address == "example.org"
    assert config.port == 2080
    assert config.username == "user"
    assert config.password == "password"


def test_update_extra():
    config = SocksConfig(
        address="example.com",
        port=1080,
    )

    config.update_extra({"version": "5"})

    assert config.extra["version"] == "5"


def test_clear_extra():
    config = SocksConfig(
        address="example.com",
        port=1080,
        extra={"version": "5"},
    )

    config.clear_extra()

    assert config.extra == {}


def test_set_extra_item():
    config = SocksConfig(
        address="example.com",
        port=1080,
    )

    config.set_extra_item("version", "5")

    assert config.extra["version"] == "5"


def test_get_extra_item():
    config = SocksConfig(
        address="example.com",
        port=1080,
        extra={"version": "5"},
    )

    assert config.get_extra_item("version") == "5"
    assert config.get_extra_item("missing") is None
    assert config.get_extra_item("missing", "default") == "default"


def test_remove_extra_item():
    config = SocksConfig(
        address="example.com",
        port=1080,
        extra={"version": "5"},
    )

    config.remove_extra_item("version")

    assert config.extra == {}


def test_to_uri_roundtrip():
    config = SocksConfig(
        address="example.com",
        port=1080,
        username="user",
        password="password",
        label="test",
    )

    parsed = parse(config.to_uri())

    assert parsed == config


def test_encoded_label():
    config = SocksConfig(
        address="example.com",
        port=1080,
        username="user",
        password="password",
        label="test 1 2",
    )

    parsed = parse(config.to_uri())
    assert parsed == config
    assert config.label == "test 1 2"
    assert config.encoded_label == "test%201%202"


def test_equality():
    config1 = SocksConfig(
        address="example.com",
        port=1080,
        username="user",
        password="password",
    )

    config2 = SocksConfig(
        address="example.com",
        port=1080,
        username="user",
        password="password",
    )

    config3 = SocksConfig(
        address="example.org",
        port=1080,
        username="user",
        password="password",
    )

    assert config1 == config2
    assert config1 != config3
    assert config1 != "config1"


def test_repr():
    config = SocksConfig(
        address="example.com",
        port=1080,
    )

    assert repr(config) == "SocksConfig(protocol=<Protocol.SOCKS: 'socks'>, label=None)"


def test_to_uri_without_auth():
    config = SocksConfig(
        address="example.com",
        port=1080,
        label="test",
    )

    assert config.to_uri() == "socks://example.com:1080#test"


def test_to_uri_username_only():
    config = SocksConfig(
        address="example.com",
        port=1080,
        username="user",
        label="test",
    )

    assert config.to_uri() == "socks://user@example.com:1080#test"
