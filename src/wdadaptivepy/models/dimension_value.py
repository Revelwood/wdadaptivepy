"""wdadaptivepy model for Adaptive's Dimension Values."""

from typing import Annotated, ClassVar

from pydantic import BeforeValidator

from wdadaptivepy.models.base import (
    ClassXMLMetadata,
    FieldMetadata,
    FieldXMLMetadata,
    HierarchialAttributedMetadata,
)
from wdadaptivepy.utils.parsers import (
    int_to_str,
    str_to_str,
)
from wdadaptivepy.utils.validators import (
    int_or_none,
    str_or_none,
)


class DimensionValue(HierarchialAttributedMetadata):
    """wdadaptivepy model for Adaptive's Dimension Values.

    Attributes:
        id: Adaptive Dimension Value ID
        code: Adaptive Dimension Value Code
        name: Adaptive Dimension Value Name
        display_name: Adaptive Dimension Value Display Name
        short_name: Adaptive Dimension Value Short Name
        description: Adaptive Dimension Value Description

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
            default_parent_tag="dimension",
            default_tag="dimensionValue",
        )
    ]
