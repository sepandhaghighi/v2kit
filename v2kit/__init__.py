# -*- coding: utf-8 -*-
"""v2kit modules."""
from .params import V2KIT_VERSION, Protocol
from .functions import is_vmess, is_vless, is_trojan, is_ss
from .functions import relabel
from .functions import encode_subscription, decode_subscription
__version__ = V2KIT_VERSION

__all__ = ["is_vmess", "is_vless", "is_trojan", "is_ss", "relabel", "encode_subscription", "decode_subscription", "Protocol"]
