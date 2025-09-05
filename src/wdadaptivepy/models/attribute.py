"""wdadaptivepy model for Adaptive's Attributes."""

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
class Attribute(Metadata):
    """wdadaptivepy model for Adaptive's Attributes.

    Attributes:
        id: Adaptive Attribute ID
        name: Adaptive Attribute Name
        display_name_type: Adaptive Attribute Display Name Type
        attribute_type: Adaptive Attribute Type
        auto_create: Adaptive Attribute Auto Create
        keep_sorted: Adaptive Attribute Keep Sorted
        dimension_id: Adaptive Attribute Dimension ID
        __xml_tags: wdadaptivepy Attribute XML tags

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
    attribute_type: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "type",
            "xml_read": "type",
            "xml_update": "type",
            "xml_delete": "type",
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
    dimension_id: int | None = field(
        default=None,
        metadata={
            "validator": int_or_none,
            "xml_parser": int_to_str,
            "xml_create": "dimensionId",
            "xml_read": "dimensionId",
            "xml_update": "dimensionId",
            "xml_delete": "dimensionId",
        },
    )
    __xml_tags: ClassVar[dict[str, str | dict[str, type]]] = {
        "xml_create_parent_tag": "attributes",
        "xml_create_tag": "attribute",
        "xml_create_children": {},
        "xml_read_parent_tag": "attributes",
        "xml_read_tag": "attribute",
        "xml_read_children": {},
        "xml_update_parent_tag": "attributes",
        "xml_update_tag": "attribute",
        "xml_update_children": {},
        "xml_delete_parent_tag": "attributes",
        "xml_delete_tag": "attribute",
        "xml_delete_children": {},
    }
