"""wdadaptivepy model for Adaptive's Currencies."""

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
    nullable_int_or_none,
    str_or_none,
)


class Currency(Metadata):
    """wdadaptivepy model for Adaptive's Currencies.

    Attributes:
        id: Adaptive Currency ID
        code: Adaptive Currency Code
        precision: Adaptive Currency Precision
        is_reporting_currency: Adaptive Currency Is Reporting Currency
        user_defined: Adaptive Currency User Defined
        description: Adaptive Currency Description

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
    precision: Annotated[
        str | None,
        BeforeValidator(nullable_int_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="precision",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    is_reporting_currency: Annotated[
        bool | None,
        BeforeValidator(bool_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="isReportingCurrency",
                    serializer=bool_to_str_one_zero,
                )
            ]
        ),
    ] = None
    user_defined: Annotated[
        bool | None,
        BeforeValidator(bool_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="userDefined",
                    serializer=bool_to_str_one_zero,
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
            default_parent_tag="currencies",
            default_tag="currency",
        )
    ]
