# -*- coding: utf-8 -*-
"""v2kit errors."""


class V2kitError(Exception):
    """Base exception for all v2kit errors."""


class V2kitValidationError(V2kitError, ValueError):
    """Base class for validation errors in 2kit."""

