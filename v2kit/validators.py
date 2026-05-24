# -*- coding: utf-8 -*-
"""v2kit validators."""
from typing import Optional
import uuid
from .params import INVALID_TYPE_MESSAGE, INVALID_ALTER_ID_MESSAGE, INVALID_EMPTY_STRING_MESSAGE
from .params import INVALID_UUID_MESSAGE, INVALID_PORT_MESSAGE


def _validate_non_empty_string(
    value: str,
    field_name: str,
) -> None:
    """
    Validate non-empty string fields.

    :param value: Input value.
    :param field_name: Field display name.
    """
    if not isinstance(value, str):
        raise TypeError(INVALID_TYPE_MESSAGE.format(field=field_name, expected_type="str"))

    if len(value.strip()) == 0:
        raise ValueError(INVALID_EMPTY_STRING_MESSAGE.format(field=field_name))


def _validate_query(query: str) -> None:
    """
    Validate query string.

    :param query: URI query string.
    """
    if not isinstance(query, str):
        raise TypeError(INVALID_TYPE_MESSAGE.format(field="Query", expected_type="str"))


def _validate_tls(tls: str) -> None:
    """
    Validate TLS mode.

    :param tls: TLS value.
    """
    if not isinstance(tls, str):
        raise TypeError(INVALID_TYPE_MESSAGE.format(field="TLS", expected_type="str"))


def _validate_network(network: str) -> None:
    """
    Validate transport network.

    :param network: Network type.
    """
    _validate_non_empty_string(network, "Network")


def _validate_encryption_method(encryption_method: str) -> None:
    """
    Validate Shadowsocks method.

    :param encryption_method: Encryption method.
    """
    _validate_non_empty_string(encryption_method, "Encryption method")


def _validate_password(password: str) -> None:
    """
    Validate password.

    :param password: Password string.
    """
    _validate_non_empty_string(password, "Password")


def _validate_uuid(value: str) -> None:
    """
    Validate UUID.

    :param value: UUID string.
    """
    if not isinstance(value, str):
        raise TypeError(INVALID_TYPE_MESSAGE.format(field="UUID", expected_type="str"))

    try:
        uuid.UUID(value)
    except Exception as exc:
        raise ValueError(INVALID_UUID_MESSAGE.format(value=value)) from exc


def _validate_port(port: int) -> None:
    """
    Validate port.

    :param port: Network port.
    """
    if not isinstance(port, int):
        raise TypeError(INVALID_TYPE_MESSAGE.format(field="Port", expected_type="int"))

    if not 1 <= port <= 65535:
        raise ValueError(INVALID_PORT_MESSAGE.format(port=port))


def _validate_host(host: str) -> None:
    """
    Validate host.

    :param host: Host address.
    """
    _validate_non_empty_string(host, "Host")


def _validate_label(label: Optional[str]) -> None:
    """
    Validate label.

    :param label: Config label.
    """
    if label is None:
        return

    _validate_non_empty_string(label, "Label")


def _validate_dict(
    value: dict,
    field_name: str,
) -> None:
    """
    Validate dictionary fields.

    :param value: Input dictionary.
    :param field_name: Field display name.
    """
    if not isinstance(value, dict):
        raise TypeError(INVALID_TYPE_MESSAGE.format(field=field_name, expected_type="dict"))


def _validate_aid(aid: int) -> None:
    """
    Validate VMESS alterId.

    :param aid: AlterId value.
    """
    if not isinstance(aid, int):
        raise TypeError(INVALID_ALTER_ID_MESSAGE)

    if aid < 0:
        raise ValueError(INVALID_ALTER_ID_MESSAGE)
