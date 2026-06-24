# -*- coding: utf-8 -*-
import pytest
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
    )

    assert config.address == "example.org"
    assert config.port == 2080
    assert config.username == "user"
    assert config.password == "password"


def test_update_methods():
    config = SocksConfig(
        address="example.com",
        port=1080,
    )

    config.update_username("user")
    config.update_password("password")

    assert config.username == "user"
    assert config.password == "password"


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


def test_config_equality():
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

    assert config1 == config2


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
