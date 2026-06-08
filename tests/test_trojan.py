# -*- coding: utf-8 -*-

from v2kit import parse
from v2kit import TrojanConfig

def test_to_uri_roundtrip():
    config = TrojanConfig(
        password="password",
        address="example.com",
        port=443,
        label="test",
    )

    parsed = parse(config.to_uri())

    assert parsed == config