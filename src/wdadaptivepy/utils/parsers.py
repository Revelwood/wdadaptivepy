"""wdadaptivepy base model for Adaptive's metadata."""

from collections.abc import Sequence
from datetime import datetime


def date_to_str(value: datetime | None) -> str | None:
    """Convert Python datetime (date) to string value.

    Args:
        value: Value to convert to string

    Returns:
        String as date or None

    Raises:
        TypeError: Unexpected type

    """
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d")
    error_message = "Unexpected type for date"
    raise TypeError(error_message)


def datetime_to_str(value: datetime | None) -> str | None:
    """Convert Python datetime (datetime) to string value.

    Args:
        value: Value to convert to string

    Returns:
        String as datetime or None

    Raises:
        TypeError: Unexpected type

    """
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S.%f")
    error_message = "Unexpected type for datetime"
    raise TypeError(error_message)


def bool_to_str_one_zero(value: bool | None) -> str | None:  # NOQA: FBT001
    """Convert boolean to string value of 1 or 0.

    Args:
        value: Value to convert to 1 or 0

    Returns:
        1 or 0 or None

    Raises:
        TypeError: Unexpected type

    """
    if value is None:
        return None
    if value is True:
        return "1"
    if value is False:
        return "0"
    error_message = "Unexpected type for boolean"
    raise TypeError(error_message)


def bool_to_str_true_false(value: bool | None) -> str | None:  # NOQA: FBT001
    """Convert boolean to string of true or false.

    Args:
        value: Value to convert to true or fale

    Returns:
        true or false or None

    Raises:
        TypeError: Unexpected type

    """
    if value is None:
        return None
    if value is True:
        return "true"
    if value is False:
        return "false"
    error_message = "Unexpected type for boolean"
    raise TypeError(error_message)


def bool_to_str_y_n(value: bool | None) -> str | None:  # NOQA: FBT001
    """Convert boolean to y or n.

    Args:
        value: Value to convert to y or n

    Returns:
        y or n or None

    Raises:
        TypeError: Unexpected type

    """
    if value is None:
        return None
    if value is True:
        return "y"
    if value is False:
        return "n"
    error_message = "Unexpected type for boolean"
    raise TypeError(error_message)


def int_to_str(value: int | str | None) -> str | None:
    """Convert integer to string.

    Args:
        value: Value to convert to a string

    Returns:
        String

    Raises:
        TypeError: Unexpected type

    """
    if value is None:
        return None
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        try:
            int_value = int(value)
            return str(int_value)
        except TypeError as e:
            error_message = "Unable to convert to integer"
            raise TypeError(error_message) from e
    error_message = "Unexpected type for integer"
    raise TypeError(error_message)


def str_to_str(value: str | None) -> str | None:
    """Convert string to string.

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


def int_list_to_str(value: Sequence[int] | None) -> str | None:
    """Convert list of integers to string.

    Args:
        value: Value to convert to string

    Returns:
        Joined string from list of integers or None

    """
    if value is None:
        return value
    return ",".join([str(x) for x in value])
