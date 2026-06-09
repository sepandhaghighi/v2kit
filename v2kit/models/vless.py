# -*- coding: utf-8 -*-
"""VLESS config model."""

from urllib.parse import urlencode
from typing import Dict, Optional
from .base import BaseConfig
from ..params import Protocol
from ..validators import (
    _validate_uuid,
    _validate_port,
    _validate_address,
)


class VLESSConfig(BaseConfig):
    """
    VLESS config model.

    Represents a VLESS configuration and provides
    validation, serialization, and URI generation.
    """

    def __init__(
        self,
        uuid: str,
        address: str,
        port: int,
        label: Optional[str] = None,
        extra: Optional[Dict[str, object]] = None,
    ):
        """
        VLESS config initiator.

        :param uuid: Config UUID.
        :param address: Config address.
        :param port: Config port.
        :param label: Config label.
        :param extra: Extra dictionary.
        """
        super().__init__(
            protocol=Protocol.VLESS,
            label=label,
            extra=extra,
        )

        self._uuid = None
        self._address = None
        self._port = None

        self.update_uuid(uuid)
        self.update_address(address)
        self.update_port(port)

    @property
    def uuid(self) -> str:
        """Get the config uuid."""
        return self._uuid

    @property
    def address(self) -> str:
        """Get the config address."""
        return self._address

    @property
    def port(self) -> int:
        """Get the config port."""
        return self._port

    def update_uuid(
        self,
        uuid: str,
    ) -> "VLESSConfig":
        """
        Update UUID.

        :param uuid: New UUID.
        """
        _validate_uuid(uuid)

        self._uuid = uuid

        return self

    def update_address(
        self,
        address: str,
    ) -> "VLESSConfig":
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
    ) -> "VLESSConfig":
        """
        Update port.

        :param port: New port.
        """
        _validate_port(port)

        self._port = port

        return self

    def to_dict(self) -> dict:
        """Convert VLESS config to dictionary."""
        return {
            "protocol": "vless",
            "uuid": self.uuid,
            "address": self.address,
            "port": self.port,
            "extra": self.extra,
            "label": self.label,
        }

    def to_uri(self) -> str:
        """Convert VLESS config to URI."""
        query = (
            f"?{urlencode(self.extra)}"
            if self.extra else ""
        )

        label = (
            f"#{self.label}"
            if self.label else ""
        )

        return (
            f"vless://{self.uuid}@"
            f"{self.address}:{self.port}"
            f"{query}{label}"
        )
