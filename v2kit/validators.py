# -*- coding: utf-8 -*-
"""v2kit validators."""
from typing import Optional
import json
import base64
import uuid
from urllib.parse import urlparse
from .errors import V2kitValidationError, V2kitParseError
from .params import Protocol, DEFAULT_ENCODING
from .params import INVALID_TYPE_MESSAGE, INVALID_ALTER_ID_MESSAGE, INVALID_EMPTY_STRING_MESSAGE
from .params import INVALID_UUID_MESSAGE, INVALID_PORT_MESSAGE, INVALID_URI_FORMAT_MESSAGE
from .params import UNSUPPORTED_PROTOCOL_MESSAGE


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
        raise V2kitValidationError(INVALID_TYPE_MESSAGE.format(field=field_name, expected_type="str"))

    if len(value.strip()) == 0:
        raise V2kitValidationError(INVALID_EMPTY_STRING_MESSAGE.format(field=field_name))


def _validate_tls(tls: str) -> None:
    """
    Validate TLS mode.

    :param tls: TLS value.
    """
    if not isinstance(tls, str):
        raise V2kitValidationError(INVALID_TYPE_MESSAGE.format(field="TLS", expected_type="str"))


def _validate_network(network: str) -> None:
    """
    Validate transport network.

    :param network: Network type.
    """
    _validate_non_empty_string(network, "Network")


def _validate_encryption(encryption: str) -> None:
    """
    Validate Shadowsocks method.

    :param encryption: Encryption method.
    """
    _validate_non_empty_string(encryption, "Encryption")


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
        raise V2kitValidationError(INVALID_TYPE_MESSAGE.format(field="UUID", expected_type="str"))

    try:
        uuid.UUID(value)
    except Exception as exc:
        raise V2kitValidationError(INVALID_UUID_MESSAGE.format(value=value)) from exc


def _validate_port(port: int) -> None:
    """
    Validate port.

    :param port: Network port.
    """
    if not isinstance(port, int):
        raise V2kitValidationError(INVALID_TYPE_MESSAGE.format(field="Port", expected_type="int"))

    if not 1 <= port <= 65535:
        raise V2kitValidationError(INVALID_PORT_MESSAGE.format(port=port))


def _validate_address(address: str) -> None:
    """
    Validate address.

    :param address: Config address.
    """
    _validate_non_empty_string(address, "Address")


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
        raise V2kitValidationError(INVALID_TYPE_MESSAGE.format(field=field_name, expected_type="dict"))


def _validate_alter_id(alter_id: int) -> None:
    """
    Validate VMESS AlterId.

    :param alter_id: AlterId value.
    """
    if not isinstance(alter_id, int):
        raise V2kitValidationError(INVALID_ALTER_ID_MESSAGE)

    if alter_id < 0:
        raise V2kitValidationError(INVALID_ALTER_ID_MESSAGE)


def _validate_username(username: Optional[str]) -> None:
    """
    Validate username.

    :param username: Config username.
    """
    if username is None:
        return

    _validate_non_empty_string(username, "Username")


def _validate_uri(uri: str) -> None:
    """
    Validate V2Ray URI format.

    :param uri: V2Ray URI.
    """
    _validate_non_empty_string(uri, "URI")

    if "://" not in uri:
        raise V2kitParseError(INVALID_URI_FORMAT_MESSAGE)
    parsed = urlparse(uri)
    try:
        Protocol(parsed.scheme)
    except Exception as exc:
        raise V2kitParseError(UNSUPPORTED_PROTOCOL_MESSAGE.format(protocol=parsed.scheme)) from exc
    if parsed.scheme == Protocol.VMESS.value:
        try:
            _, encoded = uri.split("://", 1)
            encoded += "=" * (-len(encoded) % 4)
            decoded = base64.b64decode(encoded).decode(DEFAULT_ENCODING)
            data = json.loads(decoded)
            if not isinstance(data, dict):
                raise ValueError
        except Exception as exc:
            raise V2kitParseError(INVALID_URI_FORMAT_MESSAGE) from exc
