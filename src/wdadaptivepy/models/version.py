"""wdadaptivepy model for Adaptive's Versions."""

from dataclasses import dataclass, field
from typing import ClassVar

from wdadaptivepy.models.base import (
    HierchialMetadata,
    bool_or_none,
    bool_to_str_one_zero,
    bool_to_str_true_false,
    int_or_none,
    int_to_str,
    str_or_none,
    str_to_str,
)


@dataclass(eq=False)
class Version(HierchialMetadata):
    """wdadaptivepy model for Adaptive's Versions.

    Attributes:
        id: Adaptive Version ID
        name: Adaptive Version Name
        short_name: Adaptive Version Short Name
        version_type: Adaptive Version Type
        is_virtual: Adaptive Version Is Virtual
        description: Adaptive Version Description
        is_default_version: Adaptive Version Is Default Version
        is_locked: Adaptive Version Is Locked
        has_audit_trail: Adaptive Version Has Audit Trail
        enabled_for_workflow: Adaptive Version Enabled for Workflow
        is_importable: Adaptive Version Is Importable
        start_ver: Adaptive Version Start of Version
        end_ver: Adaptive Version End of Version
        start_scroll: Adaptive Version Start Scroll
        completed_values_thru: Adaptive Version Complted Values Through
        left_scroll: Adaptive Version Left Scroll
        start_plan: Adaptive Version Start Plan
        end_plan: ADaptive Version End Plan
        lock_leading: Adaptive Version Lock Leading
        is_predictive: Adaptive Version Is Predictive
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
    version_type: str | None = field(
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
    is_virtual: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_true_false,
            "xml_create": "isVirtual",
            "xml_read": "isVirtual",
            "xml_update": "isVirtual",
            "xml_delete": "isVirtual",
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
    is_default_version: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_true_false,
            "xml_create": "isDefaultVersion",
            "xml_read": "isDefaultVersion",
            "xml_update": "isDefaultVersion",
            "xml_delete": "isDefaultVersion",
        },
    )
    is_locked: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_true_false,
            "xml_create": "isLocked",
            "xml_read": "isLocked",
            "xml_update": "isLocked",
            "xml_delete": "isLocked",
        },
    )
    has_audit_trail: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_true_false,
            "xml_create": "hasAuditTrail",
            "xml_read": "hasAuditTrail",
            "xml_update": "hasAuditTrail",
            "xml_delete": "hasAuditTrail",
        },
    )
    enabled_for_workflow: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_one_zero,
            "xml_create": "enabledForWorkflow",
            "xml_read": "enabledForWorkflow",
            "xml_update": "enabledForWorkflow",
            "xml_delete": "enabledForWorkflow",
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
    start_ver: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "startVer",
            "xml_read": "startVer",
            "xml_update": "startVer",
            "xml_delete": "startVer",
        },
    )
    end_ver: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "endVer",
            "xml_read": "endVer",
            "xml_update": "endVer",
            "xml_delete": "endVer",
        },
    )
    start_scroll: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "startScroll",
            "xml_read": "startScroll",
            "xml_update": "startScroll",
            "xml_delete": "startScroll",
        },
    )
    completed_values_thru: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "completedValuesThru",
            "xml_read": "completedValuesThru",
            "xml_update": "completedValuesThru",
            "xml_delete": "completedValuesThru",
        },
    )
    left_scroll: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "leftScroll",
            "xml_read": "leftScroll",
            "xml_update": "leftScroll",
            "xml_delete": "leftScroll",
        },
    )
    start_plan: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "startPlan",
            "xml_read": "startPlan",
            "xml_update": "startPlan",
            "xml_delete": "startPlan",
        },
    )
    end_plan: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "endPlan",
            "xml_read": "endPlan",
            "xml_update": "endPlan",
            "xml_delete": "endPlan",
        },
    )
    lock_leading: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "lockLeading",
            "xml_read": "lockLeading",
            "xml_update": "lockLeading",
            "xml_delete": "lockLeading",
        },
    )
    is_predictive: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_true_false,
            "xml_create": "isPredictive",
            "xml_read": "isPredictive",
            "xml_update": "isPredictive",
            "xml_delete": "isPredictive",
        },
    )
    __xml_tags: ClassVar[dict[str, str | dict[str, type]]] = {
        "xml_create_parent_tag": "versions",
        "xml_create_tag": "version",
        "xml_create_children": {},
        "xml_read_parent_tag": "versions",
        "xml_read_tag": "version",
        "xml_read_children": {},
        "xml_update_parent_tag": "versions",
        "xml_update_tag": "version",
        "xml_update_children": {},
        "xml_delete_parent_tag": "versions",
        "xml_delete_tag": "version",
        "xml_delete_children": {},
    }
