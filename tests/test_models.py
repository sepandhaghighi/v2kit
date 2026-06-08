# -*- coding: utf-8 -*-
from v2kit import parse
from v2kit import VMESSConfig, VLESSConfig
from v2kit import TrojanConfig, ShadowsocksConfig, SocksConfig











def test_shadowsocks_to_uri_roundtrip():
    config = ShadowsocksConfig(
        encryption="aes-256-gcm",
        password="password",
        address="example.com",
        port=8388,
        label="test",
    )

    parsed = parse(config.to_uri())

    assert parsed == config


















