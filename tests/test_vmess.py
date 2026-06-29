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


def test_extra():
    config = VMESSConfig(
        uuid="1c4b4bca-e3ff-4ca8-a062-6f399ad3cf45",
        address="example.com",
        port=443,
        extra={
            "type": "none",
            "host": "cdn.example.com",
        },
    )

    data = config.to_dict()

    assert data["type"] == "none"
    assert data["host"] == "cdn.example.com"


def test_equality():
    config1 = VMESSConfig(
        uuid="1c4b4bca-e3ff-4ca8-a062-6f399ad3cf45",
        address="example.com",
        port=443,
    )

    config2 = VMESSConfig(
        uuid="1c4b4bca-e3ff-4ca8-a062-6f399ad3cf45",
        address="example.com",
        port=443,
    )

    config3 = VMESSConfig(
        uuid="1c4b4bca-e3ff-4ca8-a062-6f399ad3cf45",
        address="example.org",
        port=443,
    )

    assert config1 == config2
    assert config1 != config3
    assert config1 != "config1"


def test_method_chaining():
    config = VMESSConfig(
        uuid="1c4b4bca-e3ff-4ca8-a062-6f399ad3cf45",
        address="example.com",
        port=443,
    )

    config.update_network("ws").update_tls("tls").update_alter_id(1)

    assert config.network == "ws"
    assert config.tls == "tls"
    assert config.alter_id == 1


@pytest.mark.parametrize(
    "kwargs",
    [
        {"uuid": "invalid"},
        {"uuid": 2},
        {"address": ""},
        {"port": 0},
        {"port": 1.2},
        {"alter_id": -1},
        {"alter_id": 2.2},
        {"network": 2},
        {"tls": 2},
        {"extra": 1}
    ],
)
def test_invalid_values(kwargs):
    params = {
        "uuid": "1c4b4bca-e3ff-4ca8-a062-6f399ad3cf45",
        "address": "example.com",
        "port": 443,
    }
    params.update(kwargs)

    with pytest.raises(ValueError):
        VMESSConfig(**params)


def test_repr():
    config = VMESSConfig(
        uuid="1c4b4bca-e3ff-4ca8-a062-6f399ad3cf45",
        address="example.com",
        port=443,
        label="test",
    )

    assert repr(config) == "VMESSConfig(protocol=<Protocol.VMESS: 'vmess'>, label='test')"


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
