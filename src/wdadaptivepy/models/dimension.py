"""wdadaptivepy model for Adaptive's Dimensions."""

from dataclasses import dataclass, field
from typing import ClassVar

from wdadaptivepy.models.base import (
    Metadata,
    bool_or_none,
    bool_to_str_one_zero,
    int_or_none,
    int_to_str,
    str_or_none,
    str_to_str,
)


@dataclass(eq=False)
class Dimension(Metadata):
    """wdadaptivepy model for Adaptive's Dimensions.

    Attributes:
        id: Adaptive Dimension ID
        name: Adaptive Dimension Name
        code: Adaptive Dimension Code
        display_name_type: ADaptive Dimension Display Name Type
        short_name: Adaptive Dimension Short Name
        auto_create: Adaptive Dimension Auto Create
        list_dimension: Adaptive Dimension List Dimension
        keep_sorted: Adaptive Dimension Keep Sorted
        use_on_levels: Adaptive Dimension Use On Levels
        seq_no: Adaptive Dimension Sequence Number
        description: Adaptive Dimension Description
        __xml_tags: wdadaptivepy XML tags

    """

    id: int | None = field(
        default=None,
        metadata={
            "validator": int_or_none,
            "xml_parser": int_to_str,
            "xml_create": "",
            "xml_read": "id",
            "xml_update": "id",
            "xml_delete": "id",
        },
    )
    name: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "name",
            "xml_read": "name",
            "xml_update": "name",
            "xml_delete": "name",
        },
    )
    code: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "code",
            "xml_read": "code",
            "xml_update": "code",
            "xml_delete": "code",
        },
    )
    display_name_type: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "displayNameType",
            "xml_read": "displayNameType",
            "xml_update": "displayNameType",
            "xml_delete": "displayNameType",
        },
    )
    short_name: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "shortName",
            "xml_read": "shortName",
            "xml_update": "shortName",
            "xml_delete": "shortName",
        },
    )
    auto_create: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_one_zero,
            "xml_create": "autoCreate",
            "xml_read": "autoCreate",
            "xml_update": "autoCreate",
            "xml_delete": "autoCreate",
        },
    )
    list_dimension: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_one_zero,
            "xml_create": "listDimension",
            "xml_read": "listDimension",
            "xml_update": "listDimension",
            "xml_delete": "listDimension",
        },
    )
    keep_sorted: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_one_zero,
            "xml_create": "keepSorted",
            "xml_read": "keepSorted",
            "xml_update": "keepSorted",
            "xml_delete": "keepSorted",
        },
    )
    use_on_levels: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_one_zero,
            "xml_create": "useOnLevels",
            "xml_read": "useOnLevels",
            "xml_update": "useOnLevels",
            "xml_delete": "useOnLevels",
        },
    )
    seq_no: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "seqNo",
            "xml_read": "seqNo",
            "xml_update": "seqNo",
            "xml_delete": "seqNo",
        },
    )
    description: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "description",
            "xml_read": "description",
            "xml_update": "description",
            "xml_delete": "description",
        },
    )
    __xml_tags: ClassVar[dict[str, str | dict[str, type]]] = {
        "xml_create_parent_tag": "dimensions",
        "xml_create_tag": "dimension",
        "xml_create_children": {},
        "xml_read_parent_tag": "dimensions",
        "xml_read_tag": "dimension",
        "xml_read_children": {},
        "xml_update_parent_tag": "dimensions",
        "xml_update_tag": "dimension",
        "xml_update_children": {},
        "xml_delete_parent_tag": "dimensions",
        "xml_delete_tag": "dimension",
        "xml_delete_children": {},
    }
