"""wdadaptivepy model for Adaptive's Time."""

from datetime import datetime
from functools import partial
from typing import Annotated, ClassVar

from pydantic import BeforeValidator, Field

from wdadaptivepy.models.base import (
    ClassXMLMetadata,
    FieldMetadata,
    FieldXMLMetadata,
    HierchialMetadata,
    Metadata,
)
from wdadaptivepy.models.list import MetadataList
from wdadaptivepy.utils.parsers import (
    bool_to_str_one_zero,
    date_to_str,
    int_to_str,
    str_to_str,
)
from wdadaptivepy.utils.validators import (
    bool_or_none,
    date_or_none,
    int_or_none,
    metadatalist_or_none,
    str_or_none,
)


class TimeLocale(Metadata):
    """wdadaptivepy model for Adaptive's Time Locale.

    Attributes:
        locale: Adaptive Time Locale Name
        label: Adaptive Time Locale Label
        short_name: Adaptive Time Locale Short Name

    """

    locale: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="locale",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    label: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="label",
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
    _xml_tags: ClassVar[list[ClassXMLMetadata]] = [
        ClassXMLMetadata(
            xml_version="default",
            default_parent_tag="locales",
            default_tag="locale",
        )
    ]


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

    """

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
    label: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="label",
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
    stratum_id: Annotated[
        int | None,
        BeforeValidator(int_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="stratumId",
                    serializer=int_to_str,
                )
            ]
        ),
    ] = None
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
    start: Annotated[
        datetime | None,
        BeforeValidator(date_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="start",
                    serializer=date_to_str,
                )
            ]
        ),
    ] = None
    end: Annotated[
        datetime | None,
        BeforeValidator(date_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="end",
                    serializer=date_to_str,
                )
            ]
        ),
    ] = None
    legacy_report_time_id: Annotated[
        int | None,
        BeforeValidator(int_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="legacyReportTimeId",
                    serializer=int_to_str,
                )
            ]
        ),
    ] = None
    legacy_sheet_time_id: Annotated[
        int | None,
        BeforeValidator(int_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="legacySheetTimeId",
                    serializer=int_to_str,
                )
            ]
        ),
    ] = None
    locales: Annotated[
        MetadataList[TimeLocale],
        BeforeValidator(partial(metadatalist_or_none, data_type=TimeLocale)),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="locales",
                    serializer=None,
                    is_child=True,
                )
            ]
        ),
    ] = Field(default_factory=MetadataList[TimeLocale])
    _xml_tags: ClassVar[list[ClassXMLMetadata]] = [
        ClassXMLMetadata(
            xml_version="default",
            default_parent_tag="periods",
            default_tag="period",
            default_children={"locales": TimeLocale},
            read_parent_tag="time",
        )
    ]


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

    """

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
    label: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="label",
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
    in_use: Annotated[
        bool | None,
        BeforeValidator(bool_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="inUse",
                    serializer=bool_to_str_one_zero,
                )
            ]
        ),
    ] = None
    is_default: Annotated[
        bool | None,
        BeforeValidator(bool_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="isDefault",
                    serializer=bool_to_str_one_zero,
                )
            ]
        ),
    ] = None
    locales: Annotated[
        MetadataList[TimeLocale],
        BeforeValidator(partial(metadatalist_or_none, data_type=TimeLocale)),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="locales",
                    serializer=None,
                    is_child=True,
                )
            ]
        ),
    ] = Field(default_factory=MetadataList[TimeLocale])
    _xml_tags: ClassVar[list[ClassXMLMetadata]] = [
        ClassXMLMetadata(
            xml_version="default",
            default_parent_tag="stratums",
            default_tag="stratum",
            default_children={"locales": TimeLocale},
            read_parent_tag="time",
        )
    ]


class Time(Metadata):
    """wdadaptivepy model for Adaptive's Time.

    Attributes:
        is_custom: Adaptive Time Is Custom
        q_first_month: Adaptive Time Quarter First Month
        last_month_is_fy: Adaptive Time Last Month Is Fiscal Year
        seq_no: Adaptive Time Sequence Number
        stratum: Adaptive Time Stratum
        period: Adaptive Time Period

    """

    is_custom: Annotated[
        bool | None,
        BeforeValidator(bool_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="isCustom",
                    serializer=bool_to_str_one_zero,
                )
            ]
        ),
    ] = None
    q_first_month: Annotated[
        int | None,
        BeforeValidator(int_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="qFirstMonth",
                    serializer=int_to_str,
                )
            ]
        ),
    ] = None
    last_month_is_fy: Annotated[
        bool | None,
        BeforeValidator(bool_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="lastMonthIsFy",
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
    stratum: Annotated[
        MetadataList[Stratum],
        BeforeValidator(partial(metadatalist_or_none, data_type=Stratum)),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="stratum",
                    serializer=None,
                    is_child=True,
                )
            ]
        ),
    ] = Field(default_factory=MetadataList[Stratum])
    period: Annotated[
        MetadataList[Period],
        BeforeValidator(partial(metadatalist_or_none, data_type=Period)),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="period",
                    serializer=None,
                    is_child=True,
                )
            ]
        ),
    ] = Field(default_factory=MetadataList[Period])
    _xml_tags: ClassVar[list[ClassXMLMetadata]] = [
        ClassXMLMetadata(
            xml_version="default",
            default_parent_tag="times",
            default_tag="time",
            default_children={"stratum": Stratum, "period": Period},
        )
    ]
