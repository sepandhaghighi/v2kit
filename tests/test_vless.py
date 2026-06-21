# -*- coding: utf-8 -*-

import pytest
from v2kit import parse
from v2kit import VLESSConfig

def test_defaults():
    config = VLESSConfig(
        uuid="1c4b4bca-e3ff-4ca8-a062-6f399ad3cf45",
        address="example.com",
        port=443,
    )

    assert config.label is None
    assert config.extra == {}


def test_to_uri_roundtrip():
    config = VLESSConfig(
        uuid="1c4b4bca-e3ff-4ca8-a062-6f399ad3cf45",
        address="example.com",
        port=443,
        label="test",
        extra={"security": "tls"},
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
