# -*- coding: utf-8 -*-
"""VMESS config model."""

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

class VMESSConfig(BaseConfig):
    """
    VMESS config model.

    Represents a VMESS configuration and provides
    validation, serialization, and URI generation.
    """

    def __init__(
        self,
        uuid: str,
        address: str,
        port: int,
        alter_id: int = 0,
        network: str = "tcp",
        tls: str = "",
        label: Optional[str] = None,
        extra: Optional[Dict[str, object]] = None,
    ):
        """
        VMESS config initiator.

        :param uuid: Config UUID.
        :param address: Config address.
        :param port: Config port.
        :param alter_id: Config AlterID.
        :param network: Config network.
        :param tls: Config TLS.
        :param label: Config label.
        :param extra: Extra dictionary.
        """
        super().__init__(
            protocol=Protocol.VMESS,
            label=label,
            extra=extra,
        )

        self._uuid = None
        self._address = None
        self._port = None

        self._alter_id = None
        self._network = None
        self._tls = None

        self.update_uuid(uuid)
        self.update_address(address)
        self.update_port(port)
        self.update_network(network)
        self.update_tls(tls)
        self.update_alter_id(alter_id)

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

    @property
    def alter_id(self) -> int:
        """Get the config AlterID."""
        return self._alter_id

    @property
    def network(self) -> str:
        """Get the config network."""
        return self._network

    @property
    def tls(self) -> str:
        """Get the config tls."""
        return self._tls

    def update_uuid(
        self,
        uuid: str,
    ) -> "VMESSConfig":
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
    ) -> "VMESSConfig":
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
    ) -> "VMESSConfig":
        """
        Update port.

        :param port: New port.
        """
        _validate_port(port)

        self._port = port

        return self

    def update_network(
        self,
        network: str,
    ) -> "VMESSConfig":
        """
        Update network.

        :param network: New network.
        """
        _validate_network(network)

        self._network = network

        return self

    def update_tls(
        self,
        tls: str,
    ) -> "VMESSConfig":
        """
        Update TLS.

        :param tls: New TLS value.
        """
        _validate_tls(tls)

        self._tls = tls

        return self

    def update_alter_id(
        self,
        alter_id: int,
    ) -> "VMESSConfig":
        """
        Update AlterId.

        :param alter_id: New AlterId.
        """
        _validate_alter_id(alter_id)

        self._alter_id = alter_id

        return self

    def to_dict(self) -> dict:
        """Convert VMESS config to dictionary."""
        data = self.extra.copy()

        data.update({
            "v": "2",
            "ps": self.label or "",
            "add": self.address,
            "port": str(self.port),
            "id": self.uuid,
            "aid": str(self.alter_id),
            "net": self.network,
            "tls": self.tls,
        })

        return data

    def to_uri(self) -> str:
        """Convert VMESS config to URI."""
        encoded = _encode_base64(
            json.dumps(
                self.to_dict(),
                ensure_ascii=False,
            )
        )

        return f"vmess://{encoded}"