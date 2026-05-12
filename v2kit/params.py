# -*- coding: utf-8 -*-
"""v2kit params."""
from enum import Enum

V2KIT_VERSION = "0.1"


class Protocol(str, Enum):
    """
    Supported V2Ray protocols.
    """

    VMESS = "vmess"
    VLESS = "vless"
    TROJAN = "trojan"
    SHADOWSOCKS = "ss"


SUPPORTED_PROTOCOLS = {item.value for item in Protocol}

DEFAULT_ENCODING = "utf-8"