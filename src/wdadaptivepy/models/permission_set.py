"""wdadaptivepy model for Adaptive's Permission Sets."""

from dataclasses import dataclass, field
from typing import ClassVar

from wdadaptivepy.models.base import (
    Metadata,
    int_or_none,
    int_to_str,
    str_or_none,
    str_to_str,
)


@dataclass(eq=False)
class PermissionSet(Metadata):
    """wdadaptivepy model for Adaptive's Permission Sets.

    Attributes:
        id: Adaptive Permission Set ID
        name: Adaptive Permission Set Name
        permissions: Adaptive Permission Set Permissions
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
    permissions: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "permissions",
            "xml_read": "permissions",
            "xml_update": "permissions",
            "xml_delete": "permissions",
        },
    )
    __xml_tags: ClassVar[dict[str, str | dict[str, type]]] = {
        "xml_create_parent_tag": "permission_sets",
        "xml_create_tag": "permission_set",
        "xml_create_children": {},
        "xml_read_parent_tag": "permission_sets",
        "xml_read_tag": "permission_set",
        "xml_read_children": {},
        "xml_update_parent_tag": "permission_sets",
        "xml_update_tag": "permission_set",
        "xml_update_children": {},
        "xml_delete_parent_tag": "permission_sets",
        "xml_delete_tag": "permission_set",
        "xml_delete_children": {},
    }
