"""wdadaptivepy base model for Adaptive's metadata."""

from collections.abc import Sequence
from datetime import datetime, timezone

from wdadaptivepy.models.list import MetadataList, T


def custom_type_or_none(value: T | Sequence[T] | None, data_type: type[T]) -> T | None:
    """Ensure a value is either a given custom Python object or None.

    Args:
        value: Value to ensure is a custom Python object or None
        data_type: Custom Python Object to check

    Returns:
        Instance of custom Python object or None

    Raises:
        TypeError: Unexpected type

    """
    if value is None:
        return None
    if isinstance(value, data_type):
        return value
    if (
        isinstance(value, Sequence)
        and len(value) <= 1
        and all(isinstance(x, data_type) for x in value)
    ):
        return value[0]
    error_message = "Unexpected data type"
    raise TypeError(error_message)


def metadatalist_or_none(
    value: Sequence[T] | None,
    data_type: type[T],
) -> MetadataList[T] | None:
    """Ensure a value is either an array of a given custom Python object or None.

    Args:
        value: Value to ensure is an array of a custom Python object or None
        data_type: Custom Python Object to check

    Returns:
        An array of custom Python object instances or None

    Raises:
        TypeError: Unexpected type

    """
    if value is None:
        return None
    if isinstance(value, Sequence) and all(isinstance(x, data_type) for x in value):
        if isinstance(value, MetadataList):
            return value
        return MetadataList[T](list(value))
    error_message = "Unexpected data type"
    raise TypeError(error_message)


def bool_or_none(value: str | int | bool | None) -> bool | None:  # NOQA: FBT001
    """Convert a value to either boolean or None.

    Args:
        value: Value to convert to boolean or None

    Returns:
        Boolean value or None

    Raises:
        ValueError: Unexpected value
        TypeError: Unexpected type

    """
    if value is None or isinstance(value, bool):
        return value
    if isinstance(value, int):
        if value == 1:
            return True
        if value == 0:
            return False
        error_message = "Invalid boolean value"
        raise ValueError(error_message)
    if isinstance(value, str):
        if value.lower() in ["true", "t", "y", "yes", "1"]:
            return True
        if value.lower() in ["false", "f", "n", "no", "0"]:
            return False
        if value == "":
            return None
        error_message = "Invalid boolean value"
        raise ValueError(error_message)
    error_message = "Unexpected type for boolean"
    raise TypeError(error_message)


def int_or_none(value: str | int | None) -> int | None:
    """Convert value to an integer or None.

    Args:
        value: Value to convert to integer or None

    Returns:
        integer or None

    Raises:
        TypeError: Unexpected type

    """
    if value is None:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        return int(value)
    error_message = "Unexpected type for integer"
    raise TypeError(error_message)


def nullable_int_or_none(value: str | int | None) -> str | None:
    """Convert integer to string.

    Args:
        value: Value to convert to string

    Returns:
        String or None

    Raises:
        TypeError: Unexpected type

    """
    if value is None:
        return None
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        if value == "":
            return value
        return str(int(value))
    error_message = "Unexpected type for integer"
    raise TypeError(error_message)


def str_or_none(value: str | None) -> str | None:
    """Convert value to string.

    Args:
        value: Value to convert to string

    Returns:
        String

    Raises:
        TypeError: Unexpected type

    """
    if value is None:
        return None
    if isinstance(value, str):
        return value
    error_message = "Unexpected type for string"
    raise TypeError(error_message)


def int_list_or_none(
    value: str | int | Sequence[int] | Sequence[str] | None,
) -> list[int] | None:
    """Convert to list of integers.

    Args:
        value: Value to convert to list of integers

    Returns:
       List of integers

    Raises:
        TypeError: Unexpected type

    """
    if value is None:
        return None
    if isinstance(value, str):
        if "," in value:
            return [int(x) for x in value.split(",")]
        return [int(value)]
    if isinstance(value, int):
        return [value]
    if isinstance(value, Sequence):
        return [int(x) for x in value]
    error_message = "unexpected type for integer list"
    raise TypeError(error_message)


def datetime_tz_or_none(dt: datetime | None) -> datetime | None:
    """Ensure a timezone exists on a datetime.

    Args:
        dt: Datetime value to check for timezone

    Returns:
        Datetime with timezone

    """
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt
