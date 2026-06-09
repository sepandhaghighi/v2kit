# -*- coding: utf-8 -*-
"""Base config model."""

from abc import ABC, abstractmethod
from typing import Dict, Optional
from ..params import Protocol
from ..validators import _validate_label, _validate_dict


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
        extra: Optional[Dict[str, object]] = None,
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
    def extra(self) -> Dict[str, object]:
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
        extra: Dict[str, object],
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
