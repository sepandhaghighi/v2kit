# -*- coding: utf-8 -*-
import pytest
from v2kit import parse
from v2kit import VMESSConfig

def test_defaults():
    config = VMESSConfig(
        uuid="1c4b4bca-e3ff-4ca8-a062-6f399ad3cf45",
        address="example.com",
        port=443,
    )

    assert config.alter_id == 0
    assert config.network == "tcp"
    assert config.tls == ""
    assert config.label is None
    assert config.extra == {}


def test_to_dict():
    config = VMESSConfig(
        uuid="1c4b4bca-e3ff-4ca8-a062-6f399ad3cf45",
        address="example.com",
        port=443,
        alter_id=1,
        network="ws",
        tls="tls",
        label="test",
    )

    assert config.to_dict() == {
        "v": "2",
        "ps": "test",
        "add": "example.com",
        "port": "443",
        "id": "1c4b4bca-e3ff-4ca8-a062-6f399ad3cf45",
        "aid": "1",
        "net": "ws",
        "tls": "tls",
    }


def test_to_uri_roundtrip():
    config = VMESSConfig(
        uuid="1c4b4bca-e3ff-4ca8-a062-6f399ad3cf45",
        address="example.com",
        port=443,
        label="test",
    )

    parsed = parse(config.to_uri())

    assert parsed == config


def test_update_methods():
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
