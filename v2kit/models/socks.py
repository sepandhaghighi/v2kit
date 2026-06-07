# -*- coding: utf-8 -*-
"""Socks config model."""

from urllib.parse import urlencode
from typing import Dict, Optional
from .base import BaseConfig
from ..params import Protocol
from ..validators import (
    _validate_port,
    _validate_address,
    _validate_label,
    _validate_password,
    _validate_username,
)

class SocksConfig(BaseConfig):
    """
    SOCKS config model.

    Represents a SOCKS configuration and provides
    validation, serialization, and URI generation.
    """

    def __init__(
        self,
        address: str,
        port: int,
        username: Optional[str] = None,
        password: Optional[str] = None,
        label: Optional[str] = None,
        extra: Optional[Dict[str, object]] = None,
    ):
        """
        SOCKS config initiator.

        :param address: Config address.
        :param port: Config port.
        :param username: Config username.
        :param password: Config password.
        :param label: Config label.
        :param extra: Extra dictionary.
        """
        super().__init__(
            protocol=Protocol.SOCKS,
            label=label,
            extra=extra,
        )

        self._address = None
        self._port = None
        self._username = None
        self._password = None

        self.update_address(address)
        self.update_port(port)
        self.update_username(username)
        self.update_password(password)

    @property
    def address(self) -> str:
        """Get the config address."""
        return self._address

    @property
    def port(self) -> int:
        """Get the config port."""
        return self._port

    @property
    def username(self) -> Optional[str]:
        """Get the config username."""
        return self._username

    @property
    def password(self) -> Optional[str]:
        """Get the config password."""
        return self._password

    def update_address(
        self,
        address: str,
    ) -> "SocksConfig":
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
    ) -> "SocksConfig":
        """
        Update port.

        :param port: New port.
        """
        _validate_port(port)
        self._port = port
        return self

    def update_username(
        self,
        username: Optional[str],
    ) -> "SocksConfig":
        """
        Update username.

        :param username: New username.
        """
        _validate_username(username)
        self._username = username
        return self

    def update_password(
        self,
        password: Optional[str],
    ) -> "SocksConfig":
        """
        Update password.

        :param password: New password.
        """
        if password is not None:
            _validate_password(password)

        self._password = password
        return self

    def to_dict(self) -> dict:
        """Convert SOCKS config to dictionary."""
        return {
            "protocol": "socks",
            "address": self.address,
            "port": self.port,
            "username": self.username,
            "password": self.password,
            "label": self.label,
            "extra": self.extra,
        }

    def to_uri(self) -> str:
        """Convert config to URI."""
        query = (
            f"?{urlencode(self.extra)}"
            if self.extra else ""
        )

        label = (
            f"#{self.label}"
            if self.label else ""
        )

        auth = ""

        if self.username:
            auth = self.username

            if self.password:
                auth += f":{self.password}"

            auth += "@"

        return (
            f"socks://"
            f"{auth}"
            f"{self.address}:{self.port}"
            f"{query}{label}"
        )