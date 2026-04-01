"""wdadaptivepy model for Adaptive's Attributes."""

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
        _xml_tags: wdadaptivepy Attribute XML tags

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
    attribute_type: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="type",
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
    dimension_id: Annotated[
        int | None,
        BeforeValidator(int_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="dimensionId",
                    serializer=int_to_str,
                )
            ]
        ),
    ] = None
    _xml_tags: ClassVar[list[ClassXMLMetadata]] = [
        ClassXMLMetadata(
            xml_version="default",
            default_parent_tag="attributes",
            default_tag="attribute",
        )
    ]
