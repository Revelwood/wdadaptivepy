"""wdadaptivepy model for Adaptive's Dimensions."""

from typing import Annotated, ClassVar

from pydantic import BeforeValidator

from wdadaptivepy.models.base import (
    ClassXMLMetadata,
    FieldMetadata,
    FieldXMLMetadata,
    Metadata,
)
from wdadaptivepy.utils.parsers import (
    bool_to_str_one_zero,
    int_to_str,
    str_to_str,
)
from wdadaptivepy.utils.validators import (
    bool_or_none,
    int_or_none,
    str_or_none,
)


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
                    xml_version="default",
                    default_tag="name",
                    serializer=str_to_str,
                )
            ]
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
    display_name_type: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="displayNameType",
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
    auto_create: Annotated[
        bool | None,
        BeforeValidator(bool_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="autoCreate",
                    serializer=bool_to_str_one_zero,
                )
            ]
        ),
    ] = None
    list_dimension: Annotated[
        bool | None,
        BeforeValidator(bool_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="listDimension",
                    serializer=bool_to_str_one_zero,
                )
            ]
        ),
    ] = None
    keep_sorted: Annotated[
        bool | None,
        BeforeValidator(bool_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="keepSorted",
                    serializer=bool_to_str_one_zero,
                )
            ]
        ),
    ] = None
    use_on_levels: Annotated[
        bool | None,
        BeforeValidator(bool_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="useOnLevels",
                    serializer=bool_to_str_one_zero,
                )
            ]
        ),
    ] = None
    seq_no: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="seqNo",
                    serializer=str_to_str,
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
    _xml_tags: ClassVar[list[ClassXMLMetadata]] = [
        ClassXMLMetadata(
            xml_version="default",
            default_parent_tag="dimensions",
            default_tag="dimension",
        )
    ]
