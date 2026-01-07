"""wdadaptivepy model for list of Adaptive metadata."""

import csv
from dataclasses import asdict
from os import PathLike
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, Protocol, TypeVar

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
                        "parent code": adaptive_parent.code,
                        "parent name": adaptive_parent.name,
                    }

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
