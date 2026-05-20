# -*- coding: utf-8 -*-
"""v2kit validators."""
from typing import Optional
import uuid


def _validate_query(query: str) -> None:
    """
    Validate query string.

    :param query: URI query string.
    """
    if not isinstance(query, str):
        raise TypeError("Query must be str.")


def _validate_tls(tls: str) -> None:
    """
    Validate TLS mode.

    :param tls: TLS value.
    """
    if not isinstance(tls, str):
        raise TypeError("TLS must be str.")


def _validate_network(network: str) -> None:
    """
    Validate transport network.

    :param network: Network type.
    """
    if not isinstance(network, str):
        raise TypeError("Network must be str.")

    if len(network.strip()) == 0:
        raise ValueError("Network cannot be empty.")


def _validate_method(method: str) -> None:
    """
    Validate Shadowsocks method.

    :param method: Encryption method.
    """
    if not isinstance(method, str):
        raise TypeError("Method must be str.")

    if len(method.strip()) == 0:
        raise ValueError("Method cannot be empty.")


def _validate_password(password: str) -> None:
    """
    Validate password.

    :param password: Password string.
    """
    if not isinstance(password, str):
        raise TypeError("Password must be str.")

    if len(password.strip()) == 0:
        raise ValueError("Password cannot be empty.")


def _validate_uuid(value: str) -> None:
    """
    Validate UUID.

    :param value: UUID string.
    """
    if not isinstance(value, str):
        raise TypeError("UUID must be str.")

    try:
        uuid.UUID(value)
    except Exception as exc:
        raise ValueError(f"Invalid UUID: {value}") from exc


def _validate_port(port: int) -> None:
    """
    Validate port.

    :param port: Network port.
    """
    if not isinstance(port, int):
        raise TypeError("Port must be int.")

    if not 1 <= port <= 65535:
        raise ValueError(f"Invalid port: {port}")


def _validate_host(host: str) -> None:
    """
    Validate host.

    :param host: Host address.
    """
    if not isinstance(host, str):
        raise TypeError("Host must be str.")

    if len(host.strip()) == 0:
        raise ValueError("Host cannot be empty.")


def _validate_label(label: Optional[str]) -> None:
    """
    Validate label.

    :param label: Config label.
    """
    if label is None:
        return

    if not isinstance(label, str):
        raise TypeError("Label must be str.")

    if len(label.strip()) == 0:
        raise ValueError("Label cannot be empty.")
