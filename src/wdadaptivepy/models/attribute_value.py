"""wdadaptivepy model for Adaptive's Attribute Values."""

from dataclasses import dataclass, field
from typing import ClassVar

from wdadaptivepy.models.base import (
    HierchialMetadata,
    int_or_none,
    int_to_str,
    str_or_none,
    str_to_str,
)


@dataclass(eq=False)
class AttributeValue(HierchialMetadata):
    """wdadaptivepy model for Adaptive's Attribute Values.

    Attributes:
        id: Adaptive Attribute Value ID
        code: Adaptive Attribute Value Code
        name: Adaptive Attribute Value Name
        display_name: Adaptive Attribute Value Display Name
        description: Adaptive Attribute Value Description
        __xml_tags: wdadaptivepy Attribute Value XML tags

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
        "xml_create_parent_tag": "attribute",
        "xml_create_tag": "attributeValue",
        "xml_create_children": {},
        "xml_read_parent_tag": "attribute",
        "xml_read_tag": "attributeValue",
        "xml_read_children": {},
        "xml_update_parent_tag": "attribute",
        "xml_update_tag": "attributeValue",
        "xml_update_children": {},
        "xml_delete_parent_tag": "attribute",
        "xml_delete_tag": "attributeValue",
        "xml_delete_children": {},
    }
