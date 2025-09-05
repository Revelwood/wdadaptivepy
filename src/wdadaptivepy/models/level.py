"""wdadaptivepy model for Adaptive's Levels."""

from dataclasses import dataclass, field
from typing import ClassVar

from wdadaptivepy.models.base import (
    HierarchialAttributedMetadata,
    bool_or_none,
    bool_to_str_one_zero,
    bool_to_str_true_false,
    int_or_none,
    int_to_str,
    str_or_none,
    str_to_str,
)


@dataclass(eq=False)
class Level(HierarchialAttributedMetadata):
    """wdadaptivepy model for Adaptive's Levels.

    Attributes:
        id: Adaptive Level ID
        code: Adaptive Level Code
        name: Adaptive Level Name
        display_name: Adaptive Level Display Name
        currency: Adaptive Level Currency
        publish_currency: Adaptive Level Publish Currency
        short_name: Adaptive Level Short Name
        available_start: Adaptive Level Available Start
        available_end: Adaptive Level Available End
        is_importable: Adaptive Level Is Importable
        workflow_status: Adaptive Level Workfalow Status
        is_elimination: Adaptive Level Is Elimination
        is_linked: Adaptive Level Is Linked
        has_children: Adaptive Level Has Children
        description: Adaptive Level Description
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
    currency: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "currency",
            "xml_read": "currency",
            "xml_update": "currency",
            "xml_delete": "currency",
        },
    )
    publish_currency: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "publishCurrency",
            "xml_read": "publishCurrency",
            "xml_update": "publishCurrency",
            "xml_delete": "publishCurrency",
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
    available_start: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "availableStart",
            "xml_read": "availableStart",
            "xml_update": "availableStart",
            "xml_delete": "availableStart",
        },
    )
    available_end: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "availableEnd",
            "xml_read": "availableEnd",
            "xml_update": "availableEnd",
            "xml_delete": "availableEnd",
        },
    )
    is_importable: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_one_zero,
            "xml_create": "isImportable",
            "xml_read": "isImportable",
            "xml_update": "isImportable",
            "xml_delete": "isImportable",
        },
    )
    workflow_status: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "workflowStatus",
            "xml_read": "workflowStatus",
            "xml_update": "workflowStatus",
            "xml_delete": "workflowStatus",
        },
    )
    is_elimination: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_one_zero,
            "xml_create": "isElimination",
            "xml_read": "isElimination",
            "xml_update": "isElimination",
            "xml_delete": "isElimination",
        },
    )
    is_linked: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_one_zero,
            "xml_create": "isLinked",
            "xml_read": "isLinked",
            "xml_update": "isLinked",
            "xml_delete": "isLinked",
        },
    )
    has_children: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_true_false,
            "xml_create": "hasChildren",
            "xml_read": "hasChildren",
            "xml_update": "hasChildren",
            "xml_delete": "hasChildren",
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
        "xml_create_parent_tag": "levels",
        "xml_create_tag": "level",
        "xml_create_children": {},
        "xml_read_parent_tag": "levels",
        "xml_read_tag": "level",
        "xml_read_children": {},
        "xml_update_parent_tag": "levels",
        "xml_update_tag": "level",
        "xml_update_children": {},
        "xml_delete_parent_tag": "levels",
        "xml_delete_tag": "level",
        "xml_delete_children": {},
    }
