"""Shadowsocks config model."""

import json
from abc import ABC, abstractmethod
from urllib.parse import urlencode
from typing import Dict, Optional
from .params import Protocol
from .validators import (
    _validate_uuid,
    _validate_port,
    _validate_address,
    _validate_label,
    _validate_password,
    _validate_encryption,
    _validate_network,
    _validate_tls,
    _validate_alter_id,
    _validate_dict,
    _validate_username,
)
from .utils import _encode_base64

class ShadowsocksConfig(BaseConfig):
    """
    Shadowsocks config model.

    Represents a Shadowsocks configuration and provides
    validation, serialization, and URI generation.
    """

    def __init__(
        self,
        encryption: str,
        password: str,
        address: str,
        port: int,
        label: Optional[str] = None,
        extra: Optional[Dict[str, object]] = None,
    ):
        """
        Shadowsocks config initiator.

        :param encryption: Config encryption method.
        :param password: Config password.
        :param address: Config address.
        :param port: Config port.
        :param label: Config label.
        :param extra: Extra dictionary.
        """
        super().__init__(
            protocol=Protocol.SHADOWSOCKS,
            label=label,
            extra=extra
        )

        self._encryption = None
        self._password = None

        self._address = None
        self._port = None

        self.update_encryption(encryption)
        self.update_password(password)
        self.update_address(address)
        self.update_port(port)

    @property
    def encryption(self) -> str:
        """Get the config encryption method."""
        return self._encryption

    @property
    def password(self) -> str:
        """Get the config password."""
        return self._password

    @property
    def address(self) -> str:
        """Get the config address."""
        return self._address

    @property
    def port(self) -> int:
        """Get the config port."""
        return self._port

    def update_encryption(
        self,
        encryption: str,
    ) -> "ShadowsocksConfig":
        """
        Update encryption method.

        :param encryption: New encryption method.
        """
        _validate_encryption(encryption)

        self._encryption = encryption

        return self

    def update_password(
        self,
        password: str,
    ) -> "ShadowsocksConfig":
        """
        Update password.

        :param password: New password.
        """
        _validate_password(password)

        self._password = password

        return self

    def update_address(
        self,
        address: str,
    ) -> "ShadowsocksConfig":
        """
        Update address.

        :param address: New address.
        """
        _validate_address(address)

        self._address = address

        return self

    def update_port(
        self,
        port: int,
    ) -> "ShadowsocksConfig":
        """
        Update port.

        :param port: New port.
        """
        _validate_port(port)

        self._port = port

        return self

    def to_dict(self) -> dict:
        """Convert Shadowsocks config to dictionary."""
        return {
            "protocol": "shadowsocks",
            "encryption": self.encryption,
            "password": self.password,
            "address": self.address,
            "port": self.port,
            "label": self.label,
            "extra": self.extra,
        }

    def to_uri(self) -> str:
        """Convert config to URI."""
        userinfo = (
            f"{self.encryption}:{self.password}"
        )

        encoded = _encode_base64(
            userinfo
        )

        label = f"#{self.label}" if self.label else ""

        return (
            f"ss://{encoded}@"
            f"{self.address}:{self.port}"
            f"{label}"
        )