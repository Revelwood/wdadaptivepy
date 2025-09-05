"""wdadaptivepy model for Adaptive's Groups."""

from dataclasses import dataclass, field
from typing import ClassVar

from wdadaptivepy.models.base import (
    Metadata,
    bool_or_none,
    bool_to_str_true_false,
    int_or_none,
    int_to_str,
    nullable_int_or_none,
    str_or_none,
    str_to_str,
)


@dataclass(eq=False)
class Group(Metadata):
    """wdadaptivepy model for Adaptive's Groups.

    Attributes:
        id: Adaptive Group ID
        name: Adaptive Group Name
        is_global: Adaptive Group Is Global
        owner_id: Adaptive Group Owner ID
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
    is_global: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_true_false,
            "xml_create": "isGlobal",
            "xml_read": "isGlobal",
            "xml_update": "isGlobal",
            "xml_delete": "isGlobal",
        },
    )
    owner_id: str | None = field(
        default=None,
        metadata={
            "validator": nullable_int_or_none,
            "xml_parser": str_to_str,
            "xml_create": "ownerId",
            "xml_read": "ownerId",
            "xml_update": "ownerId",
            "xml_delete": "ownerId",
        },
    )
    __xml_tags: ClassVar[dict[str, str | dict[str, type]]] = {
        "xml_create_parent_tag": "groups",
        "xml_create_tag": "group",
        "xml_create_children": {},
        "xml_read_parent_tag": "groups",
        "xml_read_tag": "group",
        "xml_read_children": {},
        "xml_update_parent_tag": "groups",
        "xml_update_tag": "group",
        "xml_update_children": {},
        "xml_delete_parent_tag": "groups",
        "xml_delete_tag": "group",
        "xml_delete_children": {},
    }
