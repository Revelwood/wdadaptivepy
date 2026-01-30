"""wdadaptivepy model for list of Adaptive metadata."""

import csv
import operator
import re
from collections.abc import Callable
from dataclasses import asdict
from os import PathLike
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, Protocol, Self, TypeVar

if TYPE_CHECKING:
    from datetime import datetime


class IsDataclass(Protocol):
    """Class to typehint for Data Class properties.

    Attributes:
        __dataclass_fields__: Dataclass fields

    """

    __dataclass_fields__: ClassVar[dict[str, Any]]


T = TypeVar("T", bound=IsDataclass)


class MetadataList(list[T]):
    """wdadaptivepy model for list of Adaptive metadata."""

    _OPERATORS: ClassVar[dict[str, Callable[[Any, Any], bool]]] = {
        "eq": operator.eq,
        "neq": operator.ne,
        "gt": operator.gt,
        "gte": operator.ge,
        "lt": operator.lt,
        "lte": operator.le,
        "is": operator.is_,
        "isnot": operator.is_not,
        "contains": operator.contains,
        "icontains": lambda val, q: q.lower() in val.lower(),
        "startswith": lambda val, q: val.startswith(q),
        "endswith": lambda val, q: val.endswith(q),
        "regex": lambda val, q: bool(re.search(q, val)),
    }

    def to_csv(self, file_path_and_name: str | PathLike) -> None:
        """Convert MetadataList to CSV.

        Args:
            file_path_and_name: Full path of CSV

        """
        if len(self) != 0:
            headers = list(asdict(self[0]).keys())
            if hasattr(self[0], "adaptive_parent"):
                headers.extend(["parent id", "parent code", "parent name"])

            attribute_titles: list[str] = []
            all_data: list[dict[str, str | int | bool | None | datetime]] = []
            for item in self:
                data = asdict(item)
                adaptive_parent = getattr(item, "adaptive_parent", None)
                if adaptive_parent is not None:
                    data = data | {
                        "parent id": adaptive_parent.id,
                        "parent name": adaptive_parent.name,
                    }
                    if hasattr(adaptive_parent, "code"):
                        data = data | {"parent code": adaptive_parent.code}

                adaptive_attributes = getattr(item, "adaptive_attributes", None)
                if adaptive_attributes is not None:
                    for attribute in adaptive_attributes:
                        if attribute.name + " id (attribute)" not in attribute_titles:
                            attribute_titles.append(
                                attribute.name + " id (attribute)",
                            )
                            attribute_titles.append(
                                attribute.name + " name (attribute)",
                            )
                        data = data | {
                            attribute.name + " id (attribute)": attribute.value_id,
                            attribute.name + " name (attribute)": attribute.value,
                        }
                all_data.append(data)

            headers += attribute_titles

            with Path(file_path_and_name).open("w", newline="") as csvfile:
                csv_writer = csv.DictWriter(csvfile, fieldnames=headers)
                csv_writer.writeheader()
                csv_writer.writerows(all_data)

    def get_member(self, **kwargs: Any) -> T:  # NOQA: ANN401
        """Get member from listing of members.

            **kwargs: [TODO:args]

        Returns:
            [TODO:return]

        """
        try:
            return next(item for item in self if self._matches(item, **kwargs))
        except StopIteration:
            raise ValueError from None

    def get_members(self, **kwargs: Any) -> Self:  # NOQA: ANN401
        """Get member from listing of members.

            **kwargs: [TODO:args]

        Returns:
            [TODO:return]

        """
        return self.__class__([item for item in self if self._matches(item, **kwargs)])

    def _matches(self, item: T, **kwargs: Any) -> bool:  # NOQA: ANN401
        for attr, value in kwargs.items():
            if "__" in attr:
                field_name, op_name = attr.rsplit("__", 1)
            else:
                field_name, op_name = attr, "eq"

            if not hasattr(item, field_name):
                # raise KeyError
                return False

            if op_name not in self._OPERATORS:
                raise ValueError
            op_func = self._OPERATORS[op_name]

            try:
                field_def = item.__dataclass_fields__[field_name]
                validator: Callable[[Any], Any] = field_def.metadata.get(
                    "validator",
                    lambda x: x,
                )
                new_value = validator(value)
            except KeyError as _:
                new_value = value
            if not op_func(getattr(item, field_name), new_value):
                return False

        return True
