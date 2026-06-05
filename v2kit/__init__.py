# -*- coding: utf-8 -*-
"""v2kit modules."""
from .params import V2KIT_VERSION, Protocol
from .errors import V2kitError, V2kitValidationError, V2kitParseError
from .functions import is_vmess, is_vless, is_trojan, is_shadowsocks, is_socks
from .functions import relabel
from .functions import encode_subscription, decode_subscription
from .parsers import parse
from .models import (
    VMESSConfig,
    VLESSConfig,
    TrojanConfig,
    ShadowsocksConfig,
    SocksConfig,
)
__version__ = V2KIT_VERSION

__all__ = [
    "V2kitError",
    "V2kitValidationError",
    "V2kitParseError",
    "is_vmess",
    "is_vless",
    "is_trojan",
    "is_shadowsocks",
    "is_socks",
    "relabel",
    "encode_subscription",
    "decode_subscription",
    "Protocol",
    "parse",
    "VMESSConfig",
    "VLESSConfig",
    "TrojanConfig",
    "ShadowsocksConfig",
    "SocksConfig"]
