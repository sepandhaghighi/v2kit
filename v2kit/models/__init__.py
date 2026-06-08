"""models module."""
from .base import BaseConfig
from .socks import SocksConfig
from .shadowsocks import ShadowsocksConfig
from .vless import VLESSConfig
from .vmess import VMESSConfig
from .trojan import TrojanConfig

__all__ = ["BaseConfig", "SocksConfig", "ShadowsocksConfig", "VLESSConfig", "VMESSConfig", "TrojanConfig"]
