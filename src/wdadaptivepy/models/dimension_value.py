"""wdadaptivepy model for Adaptive's Dimension Values."""

from dataclasses import dataclass, field
from typing import ClassVar

from wdadaptivepy.models.base import (
    HierarchialAttributedMetadata,
    int_or_none,
    int_to_str,
    str_or_none,
    str_to_str,
)


@dataclass(eq=False)
class DimensionValue(HierarchialAttributedMetadata):
    """wdadaptivepy model for Adaptive's Dimension Values.

    Attributes:
        id: Adaptive Dimension Value ID
        code: Adaptive Dimension Value Code
        name: Adaptive Dimension Value Name
        display_name: Adaptive Dimension Value Display Name
        short_name: Adaptive Dimension Value Short Name
        description: Adaptive Dimension Value Description
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
    display_name: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "displayName",
            "xml_read": "displayName",
            "xml_update": "displayName",
            "xml_delete": "displayName",
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
        "xml_create_parent_tag": "dimension",
        "xml_create_tag": "dimensionValue",
        "xml_create_children": {},
        "xml_read_parent_tag": "dimension",
        "xml_read_tag": "dimensionValue",
        "xml_read_children": {},
        "xml_update_parent_tag": "dimension",
        "xml_update_tag": "dimensionValue",
        "xml_update_children": {},
        "xml_delete_parent_tag": "dimension",
        "xml_delete_tag": "dimensionValue",
        "xml_delete_children": {},
    }
