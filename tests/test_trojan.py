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


def test_to_uri_roundtrip():
    config = TrojanConfig(
        password="password",
        address="example.com",
        port=443,
        label="test",
    )

    parsed = parse(config.to_uri())

    assert parsed == config
