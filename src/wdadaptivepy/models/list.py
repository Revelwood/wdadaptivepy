"""wdadaptivepy model for list of Adaptive metadata."""

import csv
import operator
import re
import sys
from collections.abc import Callable
from dataclasses import asdict
from os import PathLike
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, TypeVar, cast, get_args

from pydantic import BaseModel, BeforeValidator, GetCoreSchemaHandler
from pydantic_core import core_schema

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

if TYPE_CHECKING:
    from datetime import datetime


T = TypeVar("T", bound=BaseModel)


class MetadataList(list[T]):
    """wdadaptivepy model for list of Adaptive metadata."""

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,  # noqa: ANN401
        handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        """Define json serializer for Pydantic.

        Args:
            source_type: Data Type of values
            handler: Function to serialize data

        Returns:
            JSON schema

        """
        args = get_args(source_type)
        item_type = args[0] if args else Any
        list_schema = handler.generate_schema(list[item_type])

        return core_schema.no_info_after_validator_function(
            cls,
            list_schema,
            serialization=core_schema.plain_serializer_function_ser_schema(
                list,
                info_arg=False,
                return_schema=list_schema,  # Ensures inner models get serialized!
            ),
        )

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

    def get_member(self, **kwargs: Any) -> T | None:  # NOQA: ANN401
        """Get first member from listing of members.

        Syntax: `field_name=value` or `field_name__operator=value`

        Supported Operators:
        - __eq, __neq
        - __is, __isnot
        - __gt, __gte, __lt, __lte
        - __contains, __icontains
        - __startswith, __endswith
        - __regex

            **kwargs: keys and values to look within MetadataList

        Returns:
            Metadata Member or None

        """
        try:
            return next(item for item in self if self._matches(item, **kwargs))
        except StopIteration:
            return None

    def get_members(self, **kwargs: Any) -> Self:  # NOQA: ANN401
        """Get members from listing of members.

        Syntax: `field_name=value` or `field_name__operator=value`

        Supported Operators:
        - __eq, __neq
        - __is, __isnot
        - __gt, __gte, __lt, __lte
        - __contains, __icontains
        - __startswith, __endswith
        - __regex

            **kwargs: keys and values to look within MetadataList

        Returns:
            MetadataList

        """
        return self.__class__([item for item in self if self._matches(item, **kwargs)])

    def _matches(self, item: T, **kwargs: Any) -> bool:  # NOQA: ANN401
        for attr, value in kwargs.items():
            if "__" in attr:
                field_name, op_name = attr.rsplit("__", 1)
            else:
                field_name, op_name = attr, "eq"

            if not hasattr(item, field_name):
                raise KeyError

            if op_name not in self._OPERATORS:
                raise ValueError
            op_func = self._OPERATORS[op_name]

            field_def = item.__class__.model_fields.get(field_name)
            if not field_def:
                new_value = value
            else:
                validator = None
                for field_info in field_def.metadata:
                    if isinstance(field_info, BeforeValidator):
                        validator = cast("Callable[[Any], Any]", field_info.func)
                if not validator:
                    raise RuntimeError
                new_value = validator(value)
            if not op_func(getattr(item, field_name), new_value):
                return False

        return True
