from typing import Any, Iterable, Optional, Type
from pathlib import Path, PureWindowsPath

from nansi.utils.typings import is_optional
from nansi.utils.casting import CastError
from nansi.utils import text


def cast_pure_windows_path(
    value: Any, expected_type: Type, **context
) -> Optional[PureWindowsPath]:
    if value is None and is_optional(expected_type):
        return None
    if isinstance(value, str):
        return PureWindowsPath(value)
    if isinstance(value, PureWindowsPath):
        return value
    if isinstance(value, Iterable):
        return PureWindowsPath(*value)
    raise CastError(
        "Can't cast to PureWindowsPath, expected",
        f"{text.one_of(str, PureWindowsPath, Iterable)}, "
        f"given {text.arg('value', value)}",
        value,
        PureWindowsPath,
    )
