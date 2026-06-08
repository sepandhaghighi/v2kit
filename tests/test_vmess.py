# -*- coding: utf-8 -*-
from v2kit import parse
from v2kit import VMESSConfig

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