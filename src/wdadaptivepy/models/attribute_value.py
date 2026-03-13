"""wdadaptivepy model for Adaptive's Attribute Values."""

from typing import Annotated, ClassVar

from pydantic import BeforeValidator

from wdadaptivepy.models.base import (
    ClassXMLMetadata,
    FieldMetadata,
    FieldXMLMetadata,
    HierchialMetadata,
)
from wdadaptivepy.utils.parsers import (
    int_to_str,
    str_to_str,
)
from wdadaptivepy.utils.validators import (
    int_or_none,
    str_or_none,
)


class AttributeValue(HierchialMetadata):
    """wdadaptivepy model for Adaptive's Attribute Values.

    Attributes:
        id: Adaptive Attribute Value ID
        code: Adaptive Attribute Value Code
        name: Adaptive Attribute Value Name
        display_name: Adaptive Attribute Value Display Name
        description: Adaptive Attribute Value Description
        _xml_tags: wdadaptivepy Attribute Value XML tags

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
            default_parent_tag="attribute",
            default_tag="attributeValue",
        )
    ]
