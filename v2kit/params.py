# -*- coding: utf-8 -*-
"""v2kit params."""
from enum import Enum

V2KIT_VERSION = "0.2"


class Protocol(str, Enum):
    """Supported V2Ray protocols."""

    VMESS = "vmess"
    VLESS = "vless"
    TROJAN = "trojan"
    SHADOWSOCKS = "ss"


SUPPORTED_PROTOCOLS = {item.value for item in Protocol}

DEFAULT_ENCODING = "utf-8"

INVALID_TYPE_MESSAGE = "{field} must be {expected_type}."
INVALID_EMPTY_STRING_MESSAGE = "{field} cannot be empty."
INVALID_UUID_MESSAGE = "Invalid UUID: {value}"
INVALID_PORT_MESSAGE = "Invalid port: {port}"
INVALID_ALTER_ID_MESSAGE = "AlterId must be a non-negative integer."
INVALID_ITEMS_MESSAGE = "Items must be string or Config."
INVALID_URI_FORMAT_MESSAGE = "Invalid URI format."
INVALID_VMESS_URI_MESSAGE = "Invalid VMESS URI."
INVALID_SHADOWSOCKS_URI_MESSAGE = "Invalid Shadowsocks URI."
UNSUPPORTED_PROTOCOL_MESSAGE = "Unsupported protocol: {protocol}"
