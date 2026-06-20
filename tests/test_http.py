# -*- coding: utf-8 -*-
from v2kit import parse
from v2kit import HttpConfig


def test_update_methods():
    config = HttpConfig(
        address="example.com",
        port=1080,
    )

    config.update_username("user")
    config.update_password("password")

    assert config.username == "user"
    assert config.password == "password"


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


def test_config_equality():
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

    assert config1 == config2


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
