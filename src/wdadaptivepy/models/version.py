"""wdadaptivepy model for Adaptive's Versions."""

from typing import Annotated, ClassVar

from pydantic import BeforeValidator

from wdadaptivepy.models.base import (
    ClassXMLMetadata,
    FieldMetadata,
    FieldXMLMetadata,
    HierchialMetadata,
)
from wdadaptivepy.utils.parsers import (
    bool_to_str_one_zero,
    bool_to_str_true_false,
    int_to_str,
    str_to_str,
)
from wdadaptivepy.utils.validators import (
    bool_or_none,
    int_or_none,
    str_or_none,
)


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

    """

    id: Annotated[
        int | None,
        BeforeValidator(int_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="id",
                    create_tag="",
                    serializer=int_to_str,
                )
            ]
        ),
    ] = None
    name: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default", default_tag="name", serializer=str_to_str
                )
            ]
        ),
    ] = None
    short_name: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="shortName",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    version_type: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default", default_tag="type", serializer=str_to_str
                )
            ]
        ),
    ] = None
    is_virtual: Annotated[
        bool | None,
        BeforeValidator(bool_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="isVirtual",
                    serializer=bool_to_str_true_false,
                )
            ]
        ),
    ] = None
    description: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="description",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    is_default_version: Annotated[
        bool | None,
        BeforeValidator(bool_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="isDefaultVersion",
                    serializer=bool_to_str_true_false,
                )
            ]
        ),
    ] = None
    is_locked: Annotated[
        bool | None,
        BeforeValidator(bool_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="isLocked",
                    serializer=bool_to_str_true_false,
                )
            ]
        ),
    ] = None
    has_audit_trail: Annotated[
        bool | None,
        BeforeValidator(bool_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="hasAuditTrail",
                    serializer=bool_to_str_true_false,
                )
            ]
        ),
    ] = None
    enabled_for_workflow: Annotated[
        bool | None,
        BeforeValidator(bool_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="enabledForWorkflow",
                    serializer=bool_to_str_one_zero,
                )
            ]
        ),
    ] = None
    is_importable: Annotated[
        bool | None,
        BeforeValidator(bool_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="isImportable",
                    serializer=bool_to_str_one_zero,
                )
            ]
        ),
    ] = None
    start_ver: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default", default_tag="startVer", serializer=str_to_str
                )
            ]
        ),
    ] = None
    end_ver: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default", default_tag="endVer", serializer=str_to_str
                )
            ]
        ),
    ] = None
    start_scroll: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="startScroll",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    completed_values_thru: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="completedValuesThru",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    left_scroll: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="leftScroll",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    start_plan: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="startPlan",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    end_plan: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default", default_tag="endPlan", serializer=str_to_str
                )
            ]
        ),
    ] = None
    lock_leading: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="lockLeading",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    is_predictive: Annotated[
        bool | None,
        BeforeValidator(bool_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="isPredictive",
                    serializer=bool_to_str_true_false,
                )
            ]
        ),
    ] = None
    _xml_tags: ClassVar[list[ClassXMLMetadata]] = [
        ClassXMLMetadata(
            xml_version="default",
            default_parent_tag="versions",
            default_tag="version",
        )
    ]
