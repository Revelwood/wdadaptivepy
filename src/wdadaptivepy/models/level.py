"""wdadaptivepy model for Adaptive's Levels."""

from typing import Annotated, ClassVar

from pydantic import BeforeValidator

from wdadaptivepy.models.base import (
    ClassXMLMetadata,
    FieldMetadata,
    FieldXMLMetadata,
    HierarchialAttributedMetadata,
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
                ),
            ],
        ),
    ] = None
    code: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="code",
                    serializer=str_to_str,
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
                    xml_version="default",
                    default_tag="name",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    display_name: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="displayName",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    currency: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="currency",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    publish_currency: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="publishCurrency",
                    serializer=str_to_str,
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
    available_start: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="availableStart",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    available_end: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="availableEnd",
                    serializer=str_to_str,
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
    workflow_status: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="workflowStatus",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    is_elimination: Annotated[
        bool | None,
        BeforeValidator(bool_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="isElimination",
                    serializer=bool_to_str_one_zero,
                )
            ]
        ),
    ] = None
    is_linked: Annotated[
        bool | None,
        BeforeValidator(bool_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="isLinked",
                    serializer=bool_to_str_one_zero,
                )
            ]
        ),
    ] = None
    has_children: Annotated[
        bool | None,
        BeforeValidator(bool_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="hasChildren",
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
                ),
            ],
        ),
    ] = None
    _xml_tags: ClassVar[list[ClassXMLMetadata]] = [
        ClassXMLMetadata(
            xml_version="default",
            default_parent_tag="levels",
            default_tag="level",
        )
    ]
