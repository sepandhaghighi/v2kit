# -*- coding: utf-8 -*-
"""Trojan config model."""

import json
from abc import ABC, abstractmethod
from urllib.parse import urlencode
from typing import Dict, Optional
from .base import BaseConfig
from ..params import Protocol
from ..validators import (
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
from ..utils import _encode_base64


class TrojanConfig(BaseConfig):
    """
    Trojan config model.

    Represents a Trojan configuration and provides
    validation, serialization, and URI generation.
    """

    def __init__(
        self,
        password: str,
        address: str,
        port: int,
        label: Optional[str] = None,
        extra: Optional[Dict[str, object]] = None,
    ):
        """
        Trojan config initiator.

        :param password: Config password.
        :param address: Config address.
        :param port: Config port.
        :param label: Config label.
        :param extra: Extra dictionary.
        """
        super().__init__(
            protocol=Protocol.TROJAN,
            label=label,
            extra=extra,
        )
        self._address = None
        self._port = None
        self._password = None

        self.update_address(address)
        self.update_port(port)
        self.update_password(password)

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

    def update_password(
        self,
        password: str,
    ) -> "TrojanConfig":
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
    ) -> "TrojanConfig":
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
    ) -> "TrojanConfig":
        """
        Update port.

        :param port: New port.
        """
        _validate_port(port)

        self._port = port

        return self

    def to_dict(self) -> dict:
        """Convert Trojan config to dictionary."""
        return {
            "protocol": "trojan",
            "password": self.password,
            "address": self.address,
            "port": self.port,
            "extra": self.extra,
            "label": self.label,
        }

    def to_uri(self) -> str:
        """Convert Trojan config to URI."""
        query = (
            f"?{urlencode(self.extra)}"
            if self.extra else ""
        )

        label = (
            f"#{self.label}"
            if self.label else ""
        )

        return (
            f"trojan://{self.password}@"
            f"{self.address}:{self.port}"
            f"{query}{label}"
        )