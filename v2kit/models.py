# -*- coding: utf-8 -*-
"""v2kit models."""

import json
from abc import ABC, abstractmethod
from urllib.parse import urlencode
from typing import Optional
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
)
from .utils import _encode_base64


class BaseConfig(ABC):
    """
    Base class for all V2Ray config models.

    Provides shared validation, label management,
    and URI serialization interface.
    """

    def __init__(
        self,
        protocol: Protocol,
        label: Optional[str] = None,
        extra: Optional[dict] = None,
    ):
        """
        Config initiator.

        :param protocol: Config protocol.
        :param label: Config label.
        :param extra: Extra dictionary.
        """
        self._protocol = protocol
        self._label = None
        self._extra = {}

        self.update_extra(extra or {})
        self.update_label(label)

    @property
    def protocol(self) -> Protocol:
        """Get the config protocol."""
        return self._protocol

    @property
    def label(self) -> Optional[str]:
        """Get the config label."""
        return self._label

    @property
    def extra(self) -> dict:
        """Get extra data."""
        return self._extra

    def update_label(
        self,
        label: Optional[str],
    ):
        """
        Update config label.

        :param label: New label.
        """
        _validate_label(label)

        self._label = label

        return self

    def update_extra(
        self,
        extra: dict,
    ) -> "BaseConfig":
        """
        Update extra data.

        :param extra: Extra dictionary.
        """
        _validate_dict(
            extra,
            "Extra",
        )

        self._extra = extra

        return self

    @abstractmethod
    def to_uri(self) -> str:
        """Convert config to URI."""
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """Convert config to dictionary."""
        pass

    def __repr__(self) -> str:
        """Return string representation of BaseConfig."""
        return (
            f"{self.__class__.__name__}("
            f"protocol={self.protocol!r}, "
            f"label={self.label!r})"
        )

    def __eq__(self, other) -> bool:
        """Check configs equality."""
        if not isinstance(other, BaseConfig):
            return False
        return self.to_dict() == other.to_dict()


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
        label: Optional[str] = None,
        alter_id: int = 0,
        network: str = "tcp",
        tls: str = "",
        extra: Optional[dict] = None,
    ):
        """
        VMESS config initiator.

        :param uuid: Config UUID.
        :param address: Config address.
        :param port: Config port.
        :param label: Config label.
        :param alter_id: Config AlterID.
        :param network: Config network.
        :param tls: Config TLS.
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
        extra: Optional[dict] = None,
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
        extra: Optional[dict] = None,
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
        extra: Optional[dict] = None,
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
