# -*- coding: utf-8 -*-
import pytest
from v2kit import parse
from v2kit import HttpConfig


def test_defaults():
    config = HttpConfig(
        address="example.com",
        port=1080,
    )

    assert config.label is None
    assert config.extra == {}
    assert config.username is None
    assert config.password is None


def test_to_dict():
    config = HttpConfig(
        address="example.com",
        port=1080,
        username="user",
        password="password",
        label="test",
        extra={"foo": "bar"},
    )

    assert config.to_dict() == {
        "protocol": "http",
        "address": "example.com",
        "port": 1080,
        "username": "user",
        "password": "password",
        "extra": {"foo": "bar"},
        "label": "test",
    }


def test_extra():
    config = HttpConfig(
        address="example.com",
        port=1080,
        extra={"foo": "bar"},
    )

    data = config.to_dict()

    assert data["extra"]["foo"] == "bar"


def test_update_methods():
    config = HttpConfig(
        address="example.com",
        port=1080,
    )

    config.update_address("example.org")
    config.update_port(8080)
    config.update_username("user")
    config.update_password("password")

    assert config.address == "example.org"
    assert config.port == 8080
    assert config.username == "user"
    assert config.password == "password"


def test_update_extra():
    config = HttpConfig(
        address="example.com",
        port=1080,
    )

    config.update_extra(
        {"foo": "bar"}
    )

    assert config.extra["foo"] == "bar"


def test_method_chaining():
    config = HttpConfig(
        address="example.com",
        port=1080,
    )

    config.update_address(
        "example.org"
    ).update_port(
        8080
    ).update_username(
        "user"
    ).update_password(
        "password"
    )

    assert config.address == "example.org"
    assert config.port == 8080
    assert config.username == "user"
    assert config.password == "password"


@pytest.mark.parametrize(
    "kwargs",
    [
        {"address": ""},
        {"port": 0},
        {"username": ""},
        {"password": ""},
    ],
)
def test_invalid_values(kwargs):
    params = {
        "address": "example.com",
        "port": 1080,
    }
    params.update(kwargs)

    with pytest.raises(ValueError):
        HttpConfig(**params)


def test_to_uri_roundtrip():
    config = HttpConfig(
        address="example.com",
        port=1080,
        username="user",
        password="password",
        label="test",
    )

    parsed = parse(config.to_uri())

    assert parsed == config


def test_equality():
    config1 = HttpConfig(
        address="example.com",
        port=1080,
        username="user",
        password="password",
    )

    config2 = HttpConfig(
        address="example.com",
        port=1080,
        username="user",
        password="password",
    )

    config3 = HttpConfig(
        address="example.org",
        port=1080,
        username="user",
        password="password",
    )

    assert config1 == config2
    assert config1 != config3


def test_to_uri_without_auth():
    config = HttpConfig(
        address="example.com",
        port=1080,
        label="test",
    )

    assert config.to_uri() == "http://example.com:1080#test"


def test_to_uri_username_only():
    config = HttpConfig(
        address="example.com",
        port=1080,
        username="user",
        label="test",
    )

    assert config.to_uri() == "http://user@example.com:1080#test"


def test_repr():
    config = HttpConfig(
        address="example.com",
        port=1080,
    )

    assert repr(config) == "HttpConfig(protocol=<Protocol.HTTP: 'http'>, label=None)"
