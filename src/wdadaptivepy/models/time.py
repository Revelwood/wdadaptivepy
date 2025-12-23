"""wdadaptivepy model for Adaptive's Time."""

from dataclasses import dataclass, field
from datetime import datetime
from functools import partial
from typing import ClassVar

from wdadaptivepy.models.base import (
    HierchialMetadata,
    Metadata,
    bool_or_none,
    bool_to_str_one_zero,
    date_or_none,
    date_to_str,
    int_or_none,
    int_to_str,
    metadatalist_or_none,
    str_or_none,
    str_to_str,
)
from wdadaptivepy.models.list import MetadataList


@dataclass(eq=False)
class TimeLocale(Metadata):
    """wdadaptivepy model for Adaptive's Time Locale.

    Attributes:
        locale: Adaptive Time Locale Name
        label: Adaptive Time Locale Label
        short_name: Adaptive Time Locale Short Name
        __xml_tags: wdadaptivepy XML tags

    """

    locale: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "locale",
            "xml_read": "locale",
            "xml_update": "locale",
            "xml_delete": "locale",
        },
    )
    label: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "label",
            "xml_read": "label",
            "xml_update": "label",
            "xml_delete": "label",
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
    __xml_tags: ClassVar[dict[str, str | dict[str, type]]] = {
        "xml_create_parent_tag": "locales",
        "xml_create_tag": "locale",
        "xml_create_children": {},
        "xml_read_parent_tag": "locales",
        "xml_read_tag": "locale",
        "xml_read_children": {},
        "xml_update_parent_tag": "locales",
        "xml_update_tag": "locale",
        "xml_update_children": {},
        "xml_delete_parent_tag": "locales",
        "xml_delete_tag": "locale",
        "xml_delete_children": {},
    }


@dataclass(eq=False)
class Period(HierchialMetadata):
    """wdadaptivepy model for Adaptive's Periods.

    Attributes:
        code: Adaptive Period Code
        label: Adaptive Period Label
        short_name: Adaptive Period Short Name
        stratum_id: Adaptive Period Stratum ID
        id: Adaptive Period ID
        start: Adaptive Period Start
        end: Adaptive Period End
        legacy_report_time_id: Adaptive Period Legacy Report Time ID
        legacy_sheet_time_id: Adaptive Period Legacy Sheet Time ID
        locales: Adaptive Period Locales
        __xml_tags: wdadaptivepy XML tags

    """

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
    label: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "label",
            "xml_read": "label",
            "xml_update": "label",
            "xml_delete": "label",
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
    stratum_id: int | None = field(
        default=None,
        metadata={
            "validator": int_or_none,
            "xml_parser": int_to_str,
            "xml_create": "stratumId",
            "xml_read": "stratumId",
            "xml_update": "stratumId",
            "xml_delete": "stratumId",
        },
    )
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
    start: datetime | None = field(
        default=None,
        metadata={
            "validator": date_or_none,
            "xml_parser": date_to_str,
            "xml_create": "start",
            "xml_read": "start",
            "xml_update": "start",
            "xml_delete": "start",
        },
    )
    end: datetime | None = field(
        default=None,
        metadata={
            "validator": date_or_none,
            "xml_parser": date_to_str,
            "xml_create": "end",
            "xml_read": "end",
            "xml_update": "end",
            "xml_delete": "end",
        },
    )
    legacy_report_time_id: int | None = field(
        default=None,
        metadata={
            "validator": int_or_none,
            "xml_parser": int_to_str,
            "xml_create": "legacyReportTimeId",
            "xml_read": "legacyReportTimeId",
            "xml_update": "legacyReportTimeId",
            "xml_delete": "legacyReportTimeId",
        },
    )
    legacy_sheet_time_id: int | None = field(
        default=None,
        metadata={
            "validator": int_or_none,
            "xml_parser": int_to_str,
            "xml_create": "legacySheetTimeId",
            "xml_read": "legacySheetTimeId",
            "xml_update": "legacySheetTimeId",
            "xml_delete": "legacySheetTimeId",
        },
    )
    locales: MetadataList[TimeLocale] = field(
        default_factory=MetadataList[TimeLocale],
        metadata={
            "validator": partial(metadatalist_or_none, data_type=TimeLocale),
            "xml_parser": None,
            "xml_create": "locales",
            "xml_read": "locales",
            "xml_update": "locales",
            "xml_delete": "locales",
        },
    )
    __xml_tags: ClassVar[dict[str, str | dict[str, type]]] = {
        "xml_create_parent_tag": "periods",
        "xml_create_tag": "period",
        "xml_create_children": {"locales": TimeLocale},
        "xml_read_parent_tag": "time",
        "xml_read_tag": "period",
        "xml_read_children": {"locales": TimeLocale},
        "xml_update_parent_tag": "periods",
        "xml_update_tag": "period",
        "xml_update_children": {"locales": TimeLocale},
        "xml_delete_parent_tag": "periods",
        "xml_delete_tag": "period",
        "xml_delete_children": {"locales": TimeLocale},
    }


@dataclass(eq=False)
class Stratum(HierchialMetadata):
    """wdadaptivepy model for Adaptive's Stratum.

    Attributes:
        code: Adaptive Stratum Code
        label: Adaptive Stratum Label
        short_name: ADaptive Stratum Short Name
        id: Adaptive Stratum ID
        in_use: Adaptive Stratum In Use
        is_default: Adaptive Stratum Is Default
        locales: Adaptive Stratum Locales
        __xml_tags: wdadaptivepy XML tags

    """

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
    label: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "label",
            "xml_read": "label",
            "xml_update": "label",
            "xml_delete": "label",
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
    in_use: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_one_zero,
            "xml_create": "inUse",
            "xml_read": "inUse",
            "xml_update": "inUse",
            "xml_delete": "inUse",
        },
    )
    is_default: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_one_zero,
            "xml_create": "isDefault",
            "xml_read": "isDefault",
            "xml_update": "isDefault",
            "xml_delete": "isDefault",
        },
    )
    locales: MetadataList[TimeLocale] = field(
        default_factory=MetadataList[TimeLocale],
        metadata={
            "validator": partial(metadatalist_or_none, data_type=TimeLocale),
            "xml_parser": None,
            "xml_create": "locales",
            "xml_read": "locales",
            "xml_update": "locales",
            "xml_delete": "locales",
        },
    )
    __xml_tags: ClassVar[dict[str, str | dict[str, type]]] = {
        "xml_create_parent_tag": "stratums",
        "xml_create_tag": "stratum",
        "xml_create_children": {"locales": TimeLocale},
        "xml_read_parent_tag": "time",
        "xml_read_tag": "stratum",
        "xml_read_children": {"locales": TimeLocale},
        "xml_update_parent_tag": "stratums",
        "xml_update_tag": "stratum",
        "xml_update_children": {"locales": TimeLocale},
        "xml_delete_parent_tag": "stratums",
        "xml_delete_tag": "stratum",
        "xml_delete_children": {"locales": TimeLocale},
    }


@dataclass(eq=False)
class Time(Metadata):
    """wdadaptivepy model for Adaptive's Time.

    Attributes:
        is_custom: Adaptive Time Is Custom
        q_first_month: Adaptive Time Quarter First Month
        last_month_is_fy: Adaptive Time Last Month Is Fiscal Year
        seq_no: Adaptive Time Sequence Number
        stratum: Adaptive Time Stratum
        period: Adaptive Time Period
        __xml_tags: wdadaptivepy XML tags

    """

    is_custom: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_one_zero,
            "xml_create": "isCustom",
            "xml_read": "isCustom",
            "xml_update": "isCustom",
            "xml_delete": "isCustom",
        },
    )
    q_first_month: int | None = field(
        default=None,
        metadata={
            "validator": int_or_none,
            "xml_parser": int_to_str,
            "xml_create": "qFirstMonth",
            "xml_read": "qFirstMonth",
            "xml_update": "qFirstMonth",
            "xml_delete": "qFirstMonth",
        },
    )
    last_month_is_fy: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_one_zero,
            "xml_create": "lastMonthIsFy",
            "xml_read": "lastMonthIsFy",
            "xml_update": "lastMonthIsFy",
            "xml_delete": "lastMonthIsFy",
        },
    )
    seq_no: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "seqNo",
            "xml_read": "seqNo",
            "xml_update": "seqNo",
            "xml_delete": "seqNo",
        },
    )
    stratum: MetadataList[Stratum] = field(
        default_factory=MetadataList[Stratum],
        metadata={
            "validator": partial(metadatalist_or_none, data_type=Stratum),
            "xml_parser": None,
            "xml_create": "stratum",
            "xml_read": "stratum",
            "xml_update": "stratum",
            "xml_delete": "stratum",
        },
    )
    period: MetadataList[Period] = field(
        default_factory=MetadataList[Period],
        metadata={
            "validator": partial(metadatalist_or_none, data_type=Period),
            "xml_parser": None,
            "xml_create": "period",
            "xml_read": "period",
            "xml_update": "period",
            "xml_delete": "period",
        },
    )
    __xml_tags: ClassVar[dict[str, str | dict[str, type]]] = {
        "xml_create_parent_tag": "times",
        "xml_create_tag": "time",
        "xml_create_children": {"stratum": Stratum, "period": Period},
        "xml_read_parent_tag": "times",
        "xml_read_tag": "time",
        "xml_read_children": {"stratum": Stratum, "period": Period},
        "xml_update_parent_tag": "times",
        "xml_update_tag": "time",
        "xml_update_children": {"stratum": Stratum, "period": Period},
        "xml_delete_parent_tag": "times",
        "xml_delete_tag": "time",
        "xml_delete_children": {"stratum": Stratum, "period": Period},
    }
