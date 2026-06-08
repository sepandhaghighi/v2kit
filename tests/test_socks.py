# -*- coding: utf-8 -*-
from v2kit import parse
from v2kit import SocksConfig


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
