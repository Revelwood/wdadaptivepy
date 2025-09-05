"""wdadaptivepy model for Adaptive's Currencies."""

from dataclasses import dataclass, field
from typing import ClassVar

from wdadaptivepy.models.base import (
    Metadata,
    bool_or_none,
    bool_to_str_one_zero,
    int_or_none,
    int_to_str,
    nullable_int_or_none,
    str_or_none,
    str_to_str,
)


@dataclass(eq=False)
class Currency(Metadata):
    """wdadaptivepy model for Adaptive's Currencies.

    Attributes:
        id: Adaptive Currency ID
        code: Adaptive Currency Code
        precision: Adaptive Currency Precision
        is_reporting_currency: Adaptive Currency Is Reporting Currency
        user_defined: Adaptive Currency User Defined
        description: Adaptive Currency Description
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
    precision: str | None = field(
        default=None,
        metadata={
            "validator": nullable_int_or_none,
            "xml_parser": str_to_str,
            "xml_create": "precision",
            "xml_read": "precision",
            "xml_update": "precision",
            "xml_delete": "precision",
        },
    )
    is_reporting_currency: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_one_zero,
            "xml_create": "isReportingCurrency",
            "xml_read": "isReportingCurrency",
            "xml_update": "isReportingCurrency",
            "xml_delete": "isReportingCurrency",
        },
    )
    user_defined: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_one_zero,
            "xml_create": "userDefined",
            "xml_read": "userDefined",
            "xml_update": "userDefined",
            "xml_delete": "userDefined",
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
        "xml_create_parent_tag": "currencies",
        "xml_create_tag": "currency",
        "xml_create_children": {},
        "xml_read_parent_tag": "currencies",
        "xml_read_tag": "currency",
        "xml_read_children": {},
        "xml_update_parent_tag": "currencies",
        "xml_update_tag": "currency",
        "xml_update_children": {},
        "xml_delete_parent_tag": "currencies",
        "xml_delete_tag": "currency",
        "xml_delete_children": {},
    }
