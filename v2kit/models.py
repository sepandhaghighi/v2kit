# -*- coding: utf-8 -*-
"""v2kit models."""

import json
from typing import Optional
from .params import Protocol
from .validators import _validate_uuid, _validate_port, _validate_host, _validate_label
from .utils import _encode_base64


class BaseConfig:
    """
    Base class for all V2Ray config models.

    Provides shared validation, label management,
    and URI serialization interface.
    """

    def __init__(
        self,
        protocol: Protocol,
        label: Optional[str] = None,
    ):
        self._protocol = protocol
        self._label = None

        self.update_label(label)

    @property
    def protocol(self) -> Protocol:
        return self._protocol

    @property
    def label(self) -> Optional[str]:
        return self._label

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

    def validate(self) -> None:
        """
        Validate config fields.
        """

    def to_uri(self) -> str:
        """
        Convert config to URI.
        """
        raise NotImplementedError

    def to_dict(self) -> dict:
        """
        Convert config to dictionary.
        """
        raise NotImplementedError


class VMESSConfig(BaseConfig):
    """
    VMESS config model.

    Represents a VMESS configuration and provides
    validation, serialization, and URI generation.
    """

    def __init__(
        self,
        uuid: str,
        host: str,
        port: int,
        label: Optional[str] = None,
        aid: int = 0,
        network: str = "tcp",
        tls: str = "",
        raw_data: Optional[dict] = None,
    ):
        super().__init__(
            protocol=Protocol.VMESS,
            label=label,
        )

        self._uuid = None
        self._host = None
        self._port = None

        self._aid = aid
        self._network = network
        self._tls = tls

        self._raw_data = raw_data or {}

        self.update_uuid(uuid)
        self.update_host(host)
        self.update_port(port)

    @property
    def uuid(self) -> str:
        return self._uuid

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return self._port

    @property
    def aid(self) -> int:
        return self._aid

    @property
    def network(self) -> str:
        return self._network

    @property
    def tls(self) -> str:
        return self._tls

    def update_uuid(
        self,
        uuid: str,
    ):
        """
        Update UUID.

        :param uuid: New UUID.
        """
        _validate_uuid(uuid)

        self._uuid = uuid

        return self

    def update_host(
        self,
        host: str,
    ):
        """
        Update host.

        :param host: New host.
        """
        _validate_host(host)

        self._host = host

        return self

    def update_port(
        self,
        port: int,
    ):
        """
        Update port.

        :param port: New port.
        """
        _validate_port(port)

        self._port = port

        return self

    def validate(self) -> None:
        """
        Validate VMESS config.
        """
        _validate_uuid(self.uuid)
        _validate_host(self.host)
        _validate_port(self.port)

    def to_dict(self) -> dict:
        """
        Convert VMESS config to dictionary.
        """
        data = (
            self._raw_data.copy()
            if self._raw_data else {}
        )

        data.update({
            "v": "2",
            "ps": self.label or "",
            "add": self.host,
            "port": str(self.port),
            "id": self.uuid,
            "aid": str(self.aid),
            "net": self.network,
            "tls": self.tls,
        })

        return data

    def to_uri(self) -> str:
        """
        Convert VMESS config to URI.
        """
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
        host: str,
        port: int,
        label: Optional[str] = None,
        query: str = "",
    ):
        super().__init__(
            protocol=Protocol.VLESS,
            label=label,
        )

        self._uuid = None
        self._host = None
        self._port = None

        self._query = query

        self.update_uuid(uuid)
        self.update_host(host)
        self.update_port(port)

    @property
    def uuid(self) -> str:
        return self._uuid

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return self._port

    @property
    def query(self) -> str:
        return self._query

    def update_uuid(
        self,
        uuid: str,
    ):
        _validate_uuid(uuid)

        self._uuid = uuid

        return self

    def update_host(
        self,
        host: str,
    ):
        _validate_host(host)

        self._host = host

        return self

    def update_port(
        self,
        port: int,
    ):
        _validate_port(port)

        self._port = port

        return self

    def validate(self) -> None:
        _validate_uuid(self.uuid)
        _validate_host(self.host)
        _validate_port(self.port)

    def to_dict(self) -> dict:
        return {
            "protocol": "vless",
            "uuid": self.uuid,
            "host": self.host,
            "port": self.port,
            "query": self.query,
            "label": self.label,
        }

    def to_uri(self) -> str:
        query = (
            f"?{self.query}"
            if self.query else ""
        )

        label = (
            f"#{self.label}"
            if self.label else ""
        )

        return (
            f"vless://{self.uuid}@"
            f"{self.host}:{self.port}"
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
        host: str,
        port: int,
        label: Optional[str] = None,
        query: str = "",
    ):
        super().__init__(
            protocol=Protocol.TROJAN,
            label=label,
        )

        self._password = password
        self._host = None
        self._port = None

        self._query = query

        self.update_host(host)
        self.update_port(port)

    @property
    def password(self) -> str:
        return self._password

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return self._port

    @property
    def query(self) -> str:
        return self._query

    def update_password(
        self,
        password: str,
    ):
        """
        Update password.

        :param password: New password.
        """
        if not isinstance(password, str):
            raise TypeError("Password must be str.")

        self._password = password

        return self

    def update_host(
        self,
        host: str,
    ):
        _validate_host(host)

        self._host = host

        return self

    def update_port(
        self,
        port: int,
    ):
        _validate_port(port)

        self._port = port

        return self

    def validate(self) -> None:
        _validate_host(self.host)
        _validate_port(self.port)

    def to_dict(self) -> dict:
        return {
            "protocol": "trojan",
            "password": self.password,
            "host": self.host,
            "port": self.port,
            "query": self.query,
            "label": self.label,
        }

    def to_uri(self) -> str:
        query = (
            f"?{self.query}"
            if self.query else ""
        )

        label = (
            f"#{self.label}"
            if self.label else ""
        )

        return (
            f"trojan://{self.password}@"
            f"{self.host}:{self.port}"
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
        method: str,
        password: str,
        host: str,
        port: int,
        label: Optional[str] = None,
    ):
        super().__init__(
            protocol=Protocol.SHADOWSOCKS,
            label=label,
        )

        self._method = method
        self._password = password

        self._host = None
        self._port = None

        self.update_host(host)
        self.update_port(port)

    @property
    def method(self) -> str:
        return self._method

    @property
    def password(self) -> str:
        return self._password

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return self._port

    def update_method(
        self,
        method: str,
    ):
        """
        Update encryption method.

        :param method: New encryption method.
        """
        if not isinstance(method, str):
            raise TypeError("Method must be str.")

        self._method = method

        return self

    def update_password(
        self,
        password: str,
    ):
        if not isinstance(password, str):
            raise TypeError("Password must be str.")

        self._password = password

        return self

    def update_host(
        self,
        host: str,
    ):
        _validate_host(host)

        self._host = host

        return self

    def update_port(
        self,
        port: int,
    ):
        _validate_port(port)

        self._port = port

        return self

    def validate(self) -> None:
        _validate_host(self.host)
        _validate_port(self.port)

    def to_dict(self) -> dict:
        return {
            "protocol": "shadowsocks",
            "method": self.method,
            "password": self.password,
            "host": self.host,
            "port": self.port,
            "label": self.label,
        }

    def to_uri(self) -> str:
        """
        Convert config to URI.
        """
        userinfo = (
            f"{self.method}:{self.password}"
        )

        encoded = _encode_base64(
            userinfo
        )

        label = f"#{self.label}" if self.label else ""

        return (
            f"ss://{encoded}@"
            f"{self.host}:{self.port}"
            f"{label}"
        )