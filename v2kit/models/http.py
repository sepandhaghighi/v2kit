# -*- coding: utf-8 -*-
"""HTTP config model."""

from urllib.parse import urlencode
from typing import Dict, Optional

from .base import BaseConfig
from ..params import Protocol
from ..validators import (
    _validate_address,
    _validate_port,
    _validate_username,
    _validate_password,
)


class HTTPConfig(BaseConfig):
    """
    HTTP proxy config model.
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
        super().__init__(
            protocol=Protocol.HTTP,
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
        return self._address

    @property
    def port(self) -> int:
        return self._port

    @property
    def username(self) -> Optional[str]:
        return self._username

    @property
    def password(self) -> Optional[str]:
        return self._password

    def update_address(self, address: str) -> "HTTPConfig":
        _validate_address(address)
        self._address = address
        return self

    def update_port(self, port: int) -> "HTTPConfig":
        _validate_port(port)
        self._port = port
        return self

    def update_username(
        self,
        username: Optional[str],
    ) -> "HTTPConfig":
        _validate_username(username)
        self._username = username
        return self

    def update_password(
        self,
        password: Optional[str],
    ) -> "HTTPConfig":
        if password is not None:
            _validate_password(password)

        self._password = password
        return self

    def to_dict(self) -> dict:
        return {
            "protocol": "http",
            "address": self.address,
            "port": self.port,
            "username": self.username,
            "password": self.password,
            "extra": self.extra,
            "label": self.label,
        }

    def to_uri(self) -> str:
        auth = ""

        if self.username is not None:
            auth = self.username

            if self.password is not None:
                auth += f":{self.password}"

            auth += "@"

        query = (
            f"?{urlencode(self.extra)}"
            if self.extra else ""
        )

        label = (
            f"#{self.label}"
            if self.label else ""
        )

        return (
            f"http://{auth}"
            f"{self.address}:{self.port}"
            f"{query}{label}"
        )