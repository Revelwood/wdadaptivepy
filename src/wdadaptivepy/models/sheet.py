"""wdadaptivepy models for Adaptive's Sheets.

Covers two XML API endpoints:

- ``exportSheets`` returns the flat list of every sheet in the instance as
  ``modeled-sheet``, ``standard-sheet``, and ``cube-sheet`` elements, each with
  the light attributes ``id``, ``name``, ``code``, ``description``,
  ``isGlobal``, and ``recalculateOnDemand``.
- ``exportSheetDefinition`` returns the full definition of a single modeled or
  cube sheet, including its columns (modeled) or dimensions/users (cube).

``Sheet`` is the shared base for the three sheet variants. ``ModeledSheet`` and
``CubeSheet`` carry the richer definition-endpoint fields, which stay empty when
the object comes from the list endpoint.
"""

import sys
from dataclasses import dataclass, field
from functools import partial
from typing import ClassVar
from typing_extensions import override
from xml.etree import ElementTree as ET

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

from wdadaptivepy.models.base import (
    Metadata,
    bool_or_none,
    bool_to_str_one_zero,
    bool_to_str_true_false,
    int_list_or_none,
    int_list_to_str,
    int_or_none,
    int_to_str,
    metadatalist_or_none,
    str_or_none,
    str_to_str,
)
from wdadaptivepy.models.list import MetadataList


@dataclass(eq=False)
class Sheet(Metadata):
    """Shared base for Adaptive Sheets returned by ``exportSheets``.

    Attributes:
        id: Adaptive Sheet ID
        name: Adaptive Sheet Name
        code: Adaptive Sheet Code
        description: Adaptive Sheet Description
        is_global: Adaptive Sheet Is Global
        recalculate_on_demand: Adaptive Sheet Recalculate On Demand

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
    name: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "name",
            "xml_read": "name",
            "xml_update": "name",
            "xml_delete": "name",
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
    is_global: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_one_zero,
            "xml_create": "isGlobal",
            "xml_read": "isGlobal",
            "xml_update": "isGlobal",
            "xml_delete": "isGlobal",
        },
    )
    recalculate_on_demand: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_one_zero,
            "xml_create": "recalculateOnDemand",
            "xml_read": "recalculateOnDemand",
            "xml_update": "recalculateOnDemand",
            "xml_delete": "recalculateOnDemand",
        },
    )


@dataclass(eq=False)
class LevelRef(Metadata):
    """Reference to a Level within a Sheet column or cube dimension.

    Represents ``<level id="1" />`` nested inside a ``<levels>`` element.

    Attributes:
        id: Adaptive Level ID
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
    __xml_tags: ClassVar[dict[str, str | dict[str, type]]] = {
        "xml_create_parent_tag": "levels",
        "xml_create_tag": "level",
        "xml_create_children": {},
        "xml_read_parent_tag": "levels",
        "xml_read_tag": "level",
        "xml_read_children": {},
        "xml_update_parent_tag": "levels",
        "xml_update_tag": "level",
        "xml_update_children": {},
        "xml_delete_parent_tag": "levels",
        "xml_delete_tag": "level",
        "xml_delete_children": {},
    }


@dataclass(eq=False)
class ColumnValue(Metadata):
    """Selected value within a dimension or text-selector column.

    Represents ``<value id="19" name="E1" />``. The tag is used as its own
    parent tag so the same model can be nested under ``<dimension>`` and
    ``<text-selector>`` elements alike.

    Attributes:
        id: Adaptive Value ID
        name: Adaptive Value Name
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
    name: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "name",
            "xml_read": "name",
            "xml_update": "name",
            "xml_delete": "name",
        },
    )
    __xml_tags: ClassVar[dict[str, str | dict[str, type]]] = {
        "xml_create_parent_tag": "value",
        "xml_create_tag": "value",
        "xml_create_children": {},
        "xml_read_parent_tag": "value",
        "xml_read_tag": "value",
        "xml_read_children": {},
        "xml_update_parent_tag": "value",
        "xml_update_tag": "value",
        "xml_update_children": {},
        "xml_delete_parent_tag": "value",
        "xml_delete_tag": "value",
        "xml_delete_children": {},
    }


@dataclass(eq=False)
class ModeledSheetColumn(Metadata):
    """Shared base for the columns of a modeled sheet.

    Attributes:
        code: Adaptive Column Code
        name: Adaptive Column Name
        read_only: Adaptive Column Read Only
        splittable: Adaptive Column Splittable
        required: Adaptive Column Required
        order: 0-based position of the column within the sheet. Populated when
            the sheet is parsed from an ``exportSheetDefinition`` response
            (see :meth:`ModeledSheet.from_xml`); ``None`` otherwise. It is not
            an Adaptive XML attribute and is derived from the document order.

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
    name: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "name",
            "xml_read": "name",
            "xml_update": "name",
            "xml_delete": "name",
        },
    )
    read_only: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_true_false,
            "xml_create": "read-only",
            "xml_read": "read-only",
            "xml_update": "read-only",
            "xml_delete": "read-only",
        },
    )
    splittable: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_true_false,
            "xml_create": "splittable",
            "xml_read": "splittable",
            "xml_update": "splittable",
            "xml_delete": "splittable",
        },
    )
    required: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_true_false,
            "xml_create": "required",
            "xml_read": "required",
            "xml_update": "required",
            "xml_delete": "required",
        },
    )
    order: int | None = field(
        default=None,
        metadata={
            "validator": int_or_none,
            "xml_parser": int_to_str,
            "xml_create": "",
            "xml_read": "",
            "xml_update": "",
            "xml_delete": "",
        },
    )


@dataclass(eq=False)
class LevelsColumn(ModeledSheetColumn):
    """Modeled sheet ``<levels>`` column, listing the levels it applies to.

    Attributes:
        levels: Adaptive Levels the column applies to
        __xml_tags: wdadaptivepy XML tags

    """

    levels: MetadataList[LevelRef] = field(
        default_factory=MetadataList[LevelRef],
        metadata={
            "validator": partial(metadatalist_or_none, data_type=LevelRef),
            "xml_parser": None,
            "xml_create": "levels",
            "xml_read": "levels",
            "xml_update": "levels",
            "xml_delete": "levels",
        },
    )
    __xml_tags: ClassVar[dict[str, str | dict[str, type]]] = {
        "xml_create_parent_tag": "columns",
        "xml_create_tag": "levels",
        "xml_create_children": {"levels": LevelRef},
        "xml_read_parent_tag": "columns",
        "xml_read_tag": "levels",
        "xml_read_children": {"levels": LevelRef},
        "xml_update_parent_tag": "columns",
        "xml_update_tag": "levels",
        "xml_update_children": {"levels": LevelRef},
        "xml_delete_parent_tag": "columns",
        "xml_delete_tag": "levels",
        "xml_delete_children": {"levels": LevelRef},
    }


@dataclass(eq=False)
class TextColumn(ModeledSheetColumn):
    """Modeled sheet ``<text>`` column.

    Attributes:
        __xml_tags: wdadaptivepy XML tags

    """

    __xml_tags: ClassVar[dict[str, str | dict[str, type]]] = {
        "xml_create_parent_tag": "columns",
        "xml_create_tag": "text",
        "xml_create_children": {},
        "xml_read_parent_tag": "columns",
        "xml_read_tag": "text",
        "xml_read_children": {},
        "xml_update_parent_tag": "columns",
        "xml_update_tag": "text",
        "xml_update_children": {},
        "xml_delete_parent_tag": "columns",
        "xml_delete_tag": "text",
        "xml_delete_children": {},
    }


@dataclass(eq=False)
class DimensionColumn(ModeledSheetColumn):
    """Modeled sheet ``<dimension>`` column.

    Attributes:
        id: Adaptive Dimension ID
        values: Selected Adaptive Dimension Values
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
    values: MetadataList[ColumnValue] = field(
        default_factory=MetadataList[ColumnValue],
        metadata={
            "validator": partial(metadatalist_or_none, data_type=ColumnValue),
            "xml_parser": None,
            "xml_create": "values",
            "xml_read": "values",
            "xml_update": "values",
            "xml_delete": "values",
        },
    )
    __xml_tags: ClassVar[dict[str, str | dict[str, type]]] = {
        "xml_create_parent_tag": "columns",
        "xml_create_tag": "dimension",
        "xml_create_children": {"values": ColumnValue},
        "xml_read_parent_tag": "columns",
        "xml_read_tag": "dimension",
        "xml_read_children": {"values": ColumnValue},
        "xml_update_parent_tag": "columns",
        "xml_update_tag": "dimension",
        "xml_update_children": {"values": ColumnValue},
        "xml_delete_parent_tag": "columns",
        "xml_delete_tag": "dimension",
        "xml_delete_children": {"values": ColumnValue},
    }


@dataclass(eq=False)
class TextSelectorColumn(ModeledSheetColumn):
    """Modeled sheet ``<text-selector>`` column.

    Attributes:
        id: Adaptive Text Selector ID
        values: Selected Adaptive Text Selector Values
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
    values: MetadataList[ColumnValue] = field(
        default_factory=MetadataList[ColumnValue],
        metadata={
            "validator": partial(metadatalist_or_none, data_type=ColumnValue),
            "xml_parser": None,
            "xml_create": "values",
            "xml_read": "values",
            "xml_update": "values",
            "xml_delete": "values",
        },
    )
    __xml_tags: ClassVar[dict[str, str | dict[str, type]]] = {
        "xml_create_parent_tag": "columns",
        "xml_create_tag": "text-selector",
        "xml_create_children": {"values": ColumnValue},
        "xml_read_parent_tag": "columns",
        "xml_read_tag": "text-selector",
        "xml_read_children": {"values": ColumnValue},
        "xml_update_parent_tag": "columns",
        "xml_update_tag": "text-selector",
        "xml_update_children": {"values": ColumnValue},
        "xml_delete_parent_tag": "columns",
        "xml_delete_tag": "text-selector",
        "xml_delete_children": {"values": ColumnValue},
    }


@dataclass(eq=False)
class DateColumn(ModeledSheetColumn):
    """Modeled sheet ``<date>`` column.

    Attributes:
        __xml_tags: wdadaptivepy XML tags

    """

    __xml_tags: ClassVar[dict[str, str | dict[str, type]]] = {
        "xml_create_parent_tag": "columns",
        "xml_create_tag": "date",
        "xml_create_children": {},
        "xml_read_parent_tag": "columns",
        "xml_read_tag": "date",
        "xml_read_children": {},
        "xml_update_parent_tag": "columns",
        "xml_update_tag": "date",
        "xml_update_children": {},
        "xml_delete_parent_tag": "columns",
        "xml_delete_tag": "date",
        "xml_delete_children": {},
    }


@dataclass(eq=False)
class NumberColumn(ModeledSheetColumn):
    """Modeled sheet ``<number>`` column.

    Attributes:
        __xml_tags: wdadaptivepy XML tags

    """

    __xml_tags: ClassVar[dict[str, str | dict[str, type]]] = {
        "xml_create_parent_tag": "columns",
        "xml_create_tag": "number",
        "xml_create_children": {},
        "xml_read_parent_tag": "columns",
        "xml_read_tag": "number",
        "xml_read_children": {},
        "xml_update_parent_tag": "columns",
        "xml_update_tag": "number",
        "xml_update_children": {},
        "xml_delete_parent_tag": "columns",
        "xml_delete_tag": "number",
        "xml_delete_children": {},
    }


@dataclass(eq=False)
class InitialBalanceColumn(ModeledSheetColumn):
    """Modeled sheet ``<initial-balance>`` column.

    Attributes:
        id: Adaptive Account ID
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
    __xml_tags: ClassVar[dict[str, str | dict[str, type]]] = {
        "xml_create_parent_tag": "columns",
        "xml_create_tag": "initial-balance",
        "xml_create_children": {},
        "xml_read_parent_tag": "columns",
        "xml_read_tag": "initial-balance",
        "xml_read_children": {},
        "xml_update_parent_tag": "columns",
        "xml_update_tag": "initial-balance",
        "xml_update_children": {},
        "xml_delete_parent_tag": "columns",
        "xml_delete_tag": "initial-balance",
        "xml_delete_children": {},
    }


@dataclass(eq=False)
class DisplayColumn(ModeledSheetColumn):
    """Modeled sheet ``<display>`` column.

    Attributes:
        id: Adaptive Column ID
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
    __xml_tags: ClassVar[dict[str, str | dict[str, type]]] = {
        "xml_create_parent_tag": "columns",
        "xml_create_tag": "display",
        "xml_create_children": {},
        "xml_read_parent_tag": "columns",
        "xml_read_tag": "display",
        "xml_read_children": {},
        "xml_update_parent_tag": "columns",
        "xml_update_tag": "display",
        "xml_update_children": {},
        "xml_delete_parent_tag": "columns",
        "xml_delete_tag": "display",
        "xml_delete_children": {},
    }


@dataclass(eq=False)
class LevelCurrencyColumn(ModeledSheetColumn):
    """Modeled sheet ``<level-currency>`` column.

    Attributes:
        id: Adaptive Column ID
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
    __xml_tags: ClassVar[dict[str, str | dict[str, type]]] = {
        "xml_create_parent_tag": "columns",
        "xml_create_tag": "level-currency",
        "xml_create_children": {},
        "xml_read_parent_tag": "columns",
        "xml_read_tag": "level-currency",
        "xml_read_children": {},
        "xml_update_parent_tag": "columns",
        "xml_update_tag": "level-currency",
        "xml_update_children": {},
        "xml_delete_parent_tag": "columns",
        "xml_delete_tag": "level-currency",
        "xml_delete_children": {},
    }


@dataclass(eq=False)
class TimespanColumn(ModeledSheetColumn):
    """Modeled sheet ``<timespan>`` column.

    Attributes:
        id: Adaptive Column ID
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
    __xml_tags: ClassVar[dict[str, str | dict[str, type]]] = {
        "xml_create_parent_tag": "columns",
        "xml_create_tag": "timespan",
        "xml_create_children": {},
        "xml_read_parent_tag": "columns",
        "xml_read_tag": "timespan",
        "xml_read_children": {},
        "xml_update_parent_tag": "columns",
        "xml_update_tag": "timespan",
        "xml_update_children": {},
        "xml_delete_parent_tag": "columns",
        "xml_delete_tag": "timespan",
        "xml_delete_children": {},
    }


@dataclass(eq=False)
class StandardSheet(Sheet):
    """Adaptive Standard Sheet (only returned by ``exportSheets``).

    Attributes:
        __xml_tags: wdadaptivepy XML tags

    """

    __xml_tags: ClassVar[dict[str, str | dict[str, type]]] = {
        "xml_create_parent_tag": "sheets",
        "xml_create_tag": "standard-sheet",
        "xml_create_children": {},
        "xml_read_parent_tag": "sheets",
        "xml_read_tag": "standard-sheet",
        "xml_read_children": {},
        "xml_update_parent_tag": "sheets",
        "xml_update_tag": "standard-sheet",
        "xml_update_children": {},
        "xml_delete_parent_tag": "sheets",
        "xml_delete_tag": "standard-sheet",
        "xml_delete_children": {},
    }


@dataclass(eq=False)
class ModeledSheet(Sheet):
    """Adaptive Modeled Sheet.

    The ``available_in_actuals``, ``allow_splits``, ``split_column_title``,
    ``strata_id``, and column fields are populated by ``exportSheetDefinition``;
    they stay empty when the object comes from ``exportSheets``.

    Attributes:
        available_in_actuals: Adaptive Sheet Available In Actuals
        allow_splits: Adaptive Sheet Allow Splits
        split_column_title: Adaptive Sheet Split Column Title
        strata_id: Adaptive Sheet Strata ID
        levels_columns: Adaptive Sheet ``<levels>`` columns
        text_columns: Adaptive Sheet ``<text>`` columns
        dimension_columns: Adaptive Sheet ``<dimension>`` columns
        text_selector_columns: Adaptive Sheet ``<text-selector>`` columns
        date_columns: Adaptive Sheet ``<date>`` columns
        number_columns: Adaptive Sheet ``<number>`` columns
        initial_balance_columns: Adaptive Sheet ``<initial-balance>`` columns
        display_columns: Adaptive Sheet ``<display>`` columns
        level_currency_columns: Adaptive Sheet ``<level-currency>`` columns
        timespan_columns: Adaptive Sheet ``<timespan>`` columns
        __xml_tags: wdadaptivepy XML tags

    """

    available_in_actuals: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_true_false,
            "xml_create": "available-in-actuals",
            "xml_read": "available-in-actuals",
            "xml_update": "available-in-actuals",
            "xml_delete": "available-in-actuals",
        },
    )
    allow_splits: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_true_false,
            "xml_create": "allow-splits",
            "xml_read": "allow-splits",
            "xml_update": "allow-splits",
            "xml_delete": "allow-splits",
        },
    )
    split_column_title: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "split-column-title",
            "xml_read": "split-column-title",
            "xml_update": "split-column-title",
            "xml_delete": "split-column-title",
        },
    )
    strata_id: int | None = field(
        default=None,
        metadata={
            "validator": int_or_none,
            "xml_parser": int_to_str,
            "xml_create": "strataId",
            "xml_read": "strataId",
            "xml_update": "strataId",
            "xml_delete": "strataId",
        },
    )
    levels_columns: MetadataList[LevelsColumn] = field(
        default_factory=MetadataList[LevelsColumn],
        metadata={
            "validator": partial(metadatalist_or_none, data_type=LevelsColumn),
            "xml_parser": None,
            "xml_create": "levels_columns",
            "xml_read": "levels_columns",
            "xml_update": "levels_columns",
            "xml_delete": "levels_columns",
        },
    )
    text_columns: MetadataList[TextColumn] = field(
        default_factory=MetadataList[TextColumn],
        metadata={
            "validator": partial(metadatalist_or_none, data_type=TextColumn),
            "xml_parser": None,
            "xml_create": "text_columns",
            "xml_read": "text_columns",
            "xml_update": "text_columns",
            "xml_delete": "text_columns",
        },
    )
    dimension_columns: MetadataList[DimensionColumn] = field(
        default_factory=MetadataList[DimensionColumn],
        metadata={
            "validator": partial(metadatalist_or_none, data_type=DimensionColumn),
            "xml_parser": None,
            "xml_create": "dimension_columns",
            "xml_read": "dimension_columns",
            "xml_update": "dimension_columns",
            "xml_delete": "dimension_columns",
        },
    )
    text_selector_columns: MetadataList[TextSelectorColumn] = field(
        default_factory=MetadataList[TextSelectorColumn],
        metadata={
            "validator": partial(metadatalist_or_none, data_type=TextSelectorColumn),
            "xml_parser": None,
            "xml_create": "text_selector_columns",
            "xml_read": "text_selector_columns",
            "xml_update": "text_selector_columns",
            "xml_delete": "text_selector_columns",
        },
    )
    date_columns: MetadataList[DateColumn] = field(
        default_factory=MetadataList[DateColumn],
        metadata={
            "validator": partial(metadatalist_or_none, data_type=DateColumn),
            "xml_parser": None,
            "xml_create": "date_columns",
            "xml_read": "date_columns",
            "xml_update": "date_columns",
            "xml_delete": "date_columns",
        },
    )
    number_columns: MetadataList[NumberColumn] = field(
        default_factory=MetadataList[NumberColumn],
        metadata={
            "validator": partial(metadatalist_or_none, data_type=NumberColumn),
            "xml_parser": None,
            "xml_create": "number_columns",
            "xml_read": "number_columns",
            "xml_update": "number_columns",
            "xml_delete": "number_columns",
        },
    )
    initial_balance_columns: MetadataList[InitialBalanceColumn] = field(
        default_factory=MetadataList[InitialBalanceColumn],
        metadata={
            "validator": partial(metadatalist_or_none, data_type=InitialBalanceColumn),
            "xml_parser": None,
            "xml_create": "initial_balance_columns",
            "xml_read": "initial_balance_columns",
            "xml_update": "initial_balance_columns",
            "xml_delete": "initial_balance_columns",
        },
    )
    display_columns: MetadataList[DisplayColumn] = field(
        default_factory=MetadataList[DisplayColumn],
        metadata={
            "validator": partial(metadatalist_or_none, data_type=DisplayColumn),
            "xml_parser": None,
            "xml_create": "display_columns",
            "xml_read": "display_columns",
            "xml_update": "display_columns",
            "xml_delete": "display_columns",
        },
    )
    level_currency_columns: MetadataList[LevelCurrencyColumn] = field(
        default_factory=MetadataList[LevelCurrencyColumn],
        metadata={
            "validator": partial(metadatalist_or_none, data_type=LevelCurrencyColumn),
            "xml_parser": None,
            "xml_create": "level_currency_columns",
            "xml_read": "level_currency_columns",
            "xml_update": "level_currency_columns",
            "xml_delete": "level_currency_columns",
        },
    )
    timespan_columns: MetadataList[TimespanColumn] = field(
        default_factory=MetadataList[TimespanColumn],
        metadata={
            "validator": partial(metadatalist_or_none, data_type=TimespanColumn),
            "xml_parser": None,
            "xml_create": "timespan_columns",
            "xml_read": "timespan_columns",
            "xml_update": "timespan_columns",
            "xml_delete": "timespan_columns",
        },
    )
    __xml_tags: ClassVar[dict[str, str | dict[str, type]]] = {
        "xml_create_parent_tag": "sheets",
        "xml_create_tag": "modeled-sheet",
        "xml_create_children": {},
        "xml_read_parent_tag": "sheets",
        "xml_read_tag": "modeled-sheet",
        "xml_read_children": {
            "levels_columns": LevelsColumn,
            "text_columns": TextColumn,
            "dimension_columns": DimensionColumn,
            "text_selector_columns": TextSelectorColumn,
            "date_columns": DateColumn,
            "number_columns": NumberColumn,
            "initial_balance_columns": InitialBalanceColumn,
            "display_columns": DisplayColumn,
            "level_currency_columns": LevelCurrencyColumn,
            "timespan_columns": TimespanColumn,
        },
        "xml_update_parent_tag": "sheets",
        "xml_update_tag": "modeled-sheet",
        "xml_update_children": {},
        "xml_delete_parent_tag": "sheets",
        "xml_delete_tag": "modeled-sheet",
        "xml_delete_children": {},
    }

    @override
    @classmethod
    def from_xml(  # pyright: ignore[reportIncompatibleMethodOverride]
        cls,
        xml: ET.Element,
    ) -> "MetadataList[Self]":
        """Create ModeledSheets from XML, preserving original column order.

        The generic parser groups columns by type, which loses their original
        left-to-right order. This override records each column's 0-based
        position within the sheet's ``<columns>`` element on its ``order``
        attribute so :attr:`columns` can return them in that order.

        Args:
            xml: XML to convert to a MetadataList of ModeledSheets

        Returns:
            wdadaptivepy MetadataList of ModeledSheets

        """
        sheets = super().from_xml(xml)
        for sheet, element in zip(
            sheets,
            xml.iter("modeled-sheet"),
            strict=True,
        ):
            cls.__assign_column_order(sheet, element)
        return sheets

    @staticmethod
    def __assign_column_order(sheet: "ModeledSheet", element: ET.Element) -> None:
        """Record each column's position within the sheet's ``<columns>``.

        Args:
            sheet: The parsed ModeledSheet whose columns should be ordered
            element: The ``<modeled-sheet>`` XML element it was parsed from

        """
        columns_element = element.find("./columns")
        if columns_element is None:
            return
        tag_to_columns = {
            "levels": sheet.levels_columns,
            "text": sheet.text_columns,
            "dimension": sheet.dimension_columns,
            "text-selector": sheet.text_selector_columns,
            "date": sheet.date_columns,
            "number": sheet.number_columns,
            "initial-balance": sheet.initial_balance_columns,
            "display": sheet.display_columns,
            "level-currency": sheet.level_currency_columns,
            "timespan": sheet.timespan_columns,
        }
        counters = dict.fromkeys(tag_to_columns, 0)
        for position, child in enumerate(columns_element):
            columns = tag_to_columns.get(child.tag)
            if columns is None:
                continue
            index = counters[child.tag]
            counters[child.tag] += 1
            if index < len(columns):
                columns[index].order = position

    @property
    def columns(self) -> MetadataList[ModeledSheetColumn]:
        """All columns of the modeled sheet in their original sheet order.

        When the sheet was parsed from an ``exportSheetDefinition`` response,
        each column carries its 0-based ``order`` and the columns are returned
        in that order. For a manually built sheet whose columns have no
        ``order`` set, the columns are returned grouped by type instead.

        Returns:
            MetadataList of every column on the sheet.

        """
        combined = MetadataList[ModeledSheetColumn]()
        combined.extend(self.levels_columns)
        combined.extend(self.text_columns)
        combined.extend(self.dimension_columns)
        combined.extend(self.text_selector_columns)
        combined.extend(self.date_columns)
        combined.extend(self.number_columns)
        combined.extend(self.initial_balance_columns)
        combined.extend(self.display_columns)
        combined.extend(self.level_currency_columns)
        combined.extend(self.timespan_columns)
        if combined and all(column.order is not None for column in combined):
            return MetadataList[ModeledSheetColumn](
                sorted(combined, key=lambda column: column.order or 0),
            )
        return combined


@dataclass(eq=False)
class CubeSheetAccount(Metadata):
    """Account referenced by a cube sheet.

    Represents ``<account id="455" code="" isAssumption="false" />``.

    Attributes:
        id: Adaptive Account ID
        code: Adaptive Account Code
        is_assumption: Adaptive Account Is Assumption
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
    is_assumption: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_true_false,
            "xml_create": "isAssumption",
            "xml_read": "isAssumption",
            "xml_update": "isAssumption",
            "xml_delete": "isAssumption",
        },
    )
    __xml_tags: ClassVar[dict[str, str | dict[str, type]]] = {
        "xml_create_parent_tag": "accounts",
        "xml_create_tag": "account",
        "xml_create_children": {},
        "xml_read_parent_tag": "accounts",
        "xml_read_tag": "account",
        "xml_read_children": {},
        "xml_update_parent_tag": "accounts",
        "xml_update_tag": "account",
        "xml_update_children": {},
        "xml_delete_parent_tag": "accounts",
        "xml_delete_tag": "account",
        "xml_delete_children": {},
    }


@dataclass(eq=False)
class CubeSheetUser(Metadata):
    """User assigned to a cube sheet.

    Represents ``<user id="11" />``.

    Attributes:
        id: Adaptive User ID
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
    __xml_tags: ClassVar[dict[str, str | dict[str, type]]] = {
        "xml_create_parent_tag": "users",
        "xml_create_tag": "user",
        "xml_create_children": {},
        "xml_read_parent_tag": "users",
        "xml_read_tag": "user",
        "xml_read_children": {},
        "xml_update_parent_tag": "users",
        "xml_update_tag": "user",
        "xml_update_children": {},
        "xml_delete_parent_tag": "users",
        "xml_delete_tag": "user",
        "xml_delete_children": {},
    }


@dataclass(eq=False)
class CubeSheetDimension(Metadata):
    """Dimension of a cube sheet.

    Represents ``<dimension>`` inside a cube sheet's ``<dimensions>`` block.

    Attributes:
        id: Adaptive Dimension ID
        uncategorized: Adaptive Dimension Uncategorized
        rollup: Adaptive Dimension Rollup
        name: Adaptive Dimension Name
        new_value_behavior: Adaptive Dimension New Value Behavior
        editable_on_sheet: Adaptive Dimension Editable On Sheet
        values: Selected Adaptive Dimension Values
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
    uncategorized: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_true_false,
            "xml_create": "uncategorized",
            "xml_read": "uncategorized",
            "xml_update": "uncategorized",
            "xml_delete": "uncategorized",
        },
    )
    rollup: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_true_false,
            "xml_create": "rollup",
            "xml_read": "rollup",
            "xml_update": "rollup",
            "xml_delete": "rollup",
        },
    )
    name: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "name",
            "xml_read": "name",
            "xml_update": "name",
            "xml_delete": "name",
        },
    )
    new_value_behavior: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "newValueBehavior",
            "xml_read": "newValueBehavior",
            "xml_update": "newValueBehavior",
            "xml_delete": "newValueBehavior",
        },
    )
    editable_on_sheet: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_true_false,
            "xml_create": "editableOnSheet",
            "xml_read": "editableOnSheet",
            "xml_update": "editableOnSheet",
            "xml_delete": "editableOnSheet",
        },
    )
    values: MetadataList[ColumnValue] = field(
        default_factory=MetadataList[ColumnValue],
        metadata={
            "validator": partial(metadatalist_or_none, data_type=ColumnValue),
            "xml_parser": None,
            "xml_create": "values",
            "xml_read": "values",
            "xml_update": "values",
            "xml_delete": "values",
        },
    )
    __xml_tags: ClassVar[dict[str, str | dict[str, type]]] = {
        "xml_create_parent_tag": "dimensions",
        "xml_create_tag": "dimension",
        "xml_create_children": {"values": ColumnValue},
        "xml_read_parent_tag": "dimensions",
        "xml_read_tag": "dimension",
        "xml_read_children": {"values": ColumnValue},
        "xml_update_parent_tag": "dimensions",
        "xml_update_tag": "dimension",
        "xml_update_children": {"values": ColumnValue},
        "xml_delete_parent_tag": "dimensions",
        "xml_delete_tag": "dimension",
        "xml_delete_children": {"values": ColumnValue},
    }


@dataclass(eq=False)
class CubeSheetLevels(Metadata):
    """Levels block of a cube sheet.

    Represents ``<levels>`` inside a cube sheet's ``<dimensions>`` block.

    Attributes:
        levels: Adaptive Levels assigned to the cube sheet
        __xml_tags: wdadaptivepy XML tags

    """

    levels: MetadataList[LevelRef] = field(
        default_factory=MetadataList[LevelRef],
        metadata={
            "validator": partial(metadatalist_or_none, data_type=LevelRef),
            "xml_parser": None,
            "xml_create": "levels",
            "xml_read": "levels",
            "xml_update": "levels",
            "xml_delete": "levels",
        },
    )
    __xml_tags: ClassVar[dict[str, str | dict[str, type]]] = {
        "xml_create_parent_tag": "dimensions",
        "xml_create_tag": "levels",
        "xml_create_children": {"levels": LevelRef},
        "xml_read_parent_tag": "dimensions",
        "xml_read_tag": "levels",
        "xml_read_children": {"levels": LevelRef},
        "xml_update_parent_tag": "dimensions",
        "xml_update_tag": "levels",
        "xml_update_children": {"levels": LevelRef},
        "xml_delete_parent_tag": "dimensions",
        "xml_delete_tag": "levels",
        "xml_delete_children": {"levels": LevelRef},
    }


@dataclass(eq=False)
class CubeSheetAccounts(Metadata):
    """Accounts block of a cube sheet.

    Represents ``<accounts>`` inside a cube sheet's ``<dimensions>`` block.

    Attributes:
        accounts: Adaptive Accounts assigned to the cube sheet
        __xml_tags: wdadaptivepy XML tags

    """

    accounts: MetadataList[CubeSheetAccount] = field(
        default_factory=MetadataList[CubeSheetAccount],
        metadata={
            "validator": partial(metadatalist_or_none, data_type=CubeSheetAccount),
            "xml_parser": None,
            "xml_create": "accounts",
            "xml_read": "accounts",
            "xml_update": "accounts",
            "xml_delete": "accounts",
        },
    )
    __xml_tags: ClassVar[dict[str, str | dict[str, type]]] = {
        "xml_create_parent_tag": "dimensions",
        "xml_create_tag": "accounts",
        "xml_create_children": {"accounts": CubeSheetAccount},
        "xml_read_parent_tag": "dimensions",
        "xml_read_tag": "accounts",
        "xml_read_children": {"accounts": CubeSheetAccount},
        "xml_update_parent_tag": "dimensions",
        "xml_update_tag": "accounts",
        "xml_update_children": {"accounts": CubeSheetAccount},
        "xml_delete_parent_tag": "dimensions",
        "xml_delete_tag": "accounts",
        "xml_delete_children": {"accounts": CubeSheetAccount},
    }


@dataclass(eq=False)
class CubeSheetTime(Metadata):
    """Time configuration of a cube sheet.

    Represents ``<time initialBalance="true" visibleTimeStratumCodes="month" />``
    inside a cube sheet's ``<dimensions>`` block.

    Attributes:
        initial_balance: Adaptive Time Initial Balance
        visible_time_stratum_codes: Adaptive Visible Time Stratum Codes
        __xml_tags: wdadaptivepy XML tags

    """

    initial_balance: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_true_false,
            "xml_create": "initialBalance",
            "xml_read": "initialBalance",
            "xml_update": "initialBalance",
            "xml_delete": "initialBalance",
        },
    )
    visible_time_stratum_codes: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "visibleTimeStratumCodes",
            "xml_read": "visibleTimeStratumCodes",
            "xml_update": "visibleTimeStratumCodes",
            "xml_delete": "visibleTimeStratumCodes",
        },
    )
    __xml_tags: ClassVar[dict[str, str | dict[str, type]]] = {
        "xml_create_parent_tag": "dimensions",
        "xml_create_tag": "time",
        "xml_create_children": {},
        "xml_read_parent_tag": "dimensions",
        "xml_read_tag": "time",
        "xml_read_children": {},
        "xml_update_parent_tag": "dimensions",
        "xml_update_tag": "time",
        "xml_update_children": {},
        "xml_delete_parent_tag": "dimensions",
        "xml_delete_tag": "time",
        "xml_delete_children": {},
    }


@dataclass(eq=False)
class CubeSheetUsers(Metadata):
    """Users block of a cube sheet.

    Represents ``<users isExcludedFromWorkflow="true">`` directly under the
    cube sheet element.

    Attributes:
        is_excluded_from_workflow: Adaptive Users Is Excluded From Workflow
        users: Adaptive Users assigned to the cube sheet
        __xml_tags: wdadaptivepy XML tags

    """

    is_excluded_from_workflow: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_true_false,
            "xml_create": "isExcludedFromWorkflow",
            "xml_read": "isExcludedFromWorkflow",
            "xml_update": "isExcludedFromWorkflow",
            "xml_delete": "isExcludedFromWorkflow",
        },
    )
    users: MetadataList[CubeSheetUser] = field(
        default_factory=MetadataList[CubeSheetUser],
        metadata={
            "validator": partial(metadatalist_or_none, data_type=CubeSheetUser),
            "xml_parser": None,
            "xml_create": "users",
            "xml_read": "users",
            "xml_update": "users",
            "xml_delete": "users",
        },
    )
    __xml_tags: ClassVar[dict[str, str | dict[str, type]]] = {
        "xml_create_parent_tag": "cube-sheet",
        "xml_create_tag": "users",
        "xml_create_children": {"users": CubeSheetUser},
        "xml_read_parent_tag": "cube-sheet",
        "xml_read_tag": "users",
        "xml_read_children": {"users": CubeSheetUser},
        "xml_update_parent_tag": "cube-sheet",
        "xml_update_tag": "users",
        "xml_update_children": {"users": CubeSheetUser},
        "xml_delete_parent_tag": "cube-sheet",
        "xml_delete_tag": "users",
        "xml_delete_children": {"users": CubeSheetUser},
    }


@dataclass(eq=False)
class CubeSheet(Sheet):
    """Adaptive Cube Sheet.

    The definition fields below are populated by ``exportSheetDefinition``; they
    stay empty when the object comes from ``exportSheets``.

    Attributes:
        strata_id: Adaptive Sheet Strata ID
        horizontal_axis: Adaptive Sheet Horizontal Axis
        vertical_axis: Adaptive Sheet Vertical Axis
        max_column_width: Adaptive Sheet Max Column Width
        suppress_zero_rows: Adaptive Sheet Suppress Zero Rows
        rearrange_gl_and_custom_accounts: Adaptive Sheet Rearrange GL/Custom
        hide_rollup_totals: Adaptive Sheet Hide Rollup Totals
        dimensions: Adaptive Cube Sheet Dimensions
        levels: Adaptive Cube Sheet Levels
        accounts: Adaptive Cube Sheet Accounts
        time: Adaptive Cube Sheet Time configuration
        users: Adaptive Cube Sheet Users
        __xml_tags: wdadaptivepy XML tags

    """

    strata_id: int | None = field(
        default=None,
        metadata={
            "validator": int_or_none,
            "xml_parser": int_to_str,
            "xml_create": "strataId",
            "xml_read": "strataId",
            "xml_update": "strataId",
            "xml_delete": "strataId",
        },
    )
    horizontal_axis: int | None = field(
        default=None,
        metadata={
            "validator": int_or_none,
            "xml_parser": int_to_str,
            "xml_create": "horizontalAxis",
            "xml_read": "horizontalAxis",
            "xml_update": "horizontalAxis",
            "xml_delete": "horizontalAxis",
        },
    )
    vertical_axis: list[int] | None = field(
        default=None,
        metadata={
            "validator": int_list_or_none,
            "xml_parser": int_list_to_str,
            "xml_create": "verticalAxis",
            "xml_read": "verticalAxis",
            "xml_update": "verticalAxis",
            "xml_delete": "verticalAxis",
        },
    )
    max_column_width: int | None = field(
        default=None,
        metadata={
            "validator": int_or_none,
            "xml_parser": int_to_str,
            "xml_create": "maxColumnWidth",
            "xml_read": "maxColumnWidth",
            "xml_update": "maxColumnWidth",
            "xml_delete": "maxColumnWidth",
        },
    )
    suppress_zero_rows: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_one_zero,
            "xml_create": "suppressZeroRows",
            "xml_read": "suppressZeroRows",
            "xml_update": "suppressZeroRows",
            "xml_delete": "suppressZeroRows",
        },
    )
    rearrange_gl_and_custom_accounts: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_one_zero,
            "xml_create": "rearrangeGLAndCustomAccounts",
            "xml_read": "rearrangeGLAndCustomAccounts",
            "xml_update": "rearrangeGLAndCustomAccounts",
            "xml_delete": "rearrangeGLAndCustomAccounts",
        },
    )
    hide_rollup_totals: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_one_zero,
            "xml_create": "hideRollupTotals",
            "xml_read": "hideRollupTotals",
            "xml_update": "hideRollupTotals",
            "xml_delete": "hideRollupTotals",
        },
    )
    dimensions: MetadataList[CubeSheetDimension] = field(
        default_factory=MetadataList[CubeSheetDimension],
        metadata={
            "validator": partial(metadatalist_or_none, data_type=CubeSheetDimension),
            "xml_parser": None,
            "xml_create": "dimensions",
            "xml_read": "dimensions",
            "xml_update": "dimensions",
            "xml_delete": "dimensions",
        },
    )
    levels: MetadataList[CubeSheetLevels] = field(
        default_factory=MetadataList[CubeSheetLevels],
        metadata={
            "validator": partial(metadatalist_or_none, data_type=CubeSheetLevels),
            "xml_parser": None,
            "xml_create": "levels",
            "xml_read": "levels",
            "xml_update": "levels",
            "xml_delete": "levels",
        },
    )
    accounts: MetadataList[CubeSheetAccounts] = field(
        default_factory=MetadataList[CubeSheetAccounts],
        metadata={
            "validator": partial(metadatalist_or_none, data_type=CubeSheetAccounts),
            "xml_parser": None,
            "xml_create": "accounts",
            "xml_read": "accounts",
            "xml_update": "accounts",
            "xml_delete": "accounts",
        },
    )
    time: MetadataList[CubeSheetTime] = field(
        default_factory=MetadataList[CubeSheetTime],
        metadata={
            "validator": partial(metadatalist_or_none, data_type=CubeSheetTime),
            "xml_parser": None,
            "xml_create": "time",
            "xml_read": "time",
            "xml_update": "time",
            "xml_delete": "time",
        },
    )
    users: MetadataList[CubeSheetUsers] = field(
        default_factory=MetadataList[CubeSheetUsers],
        metadata={
            "validator": partial(metadatalist_or_none, data_type=CubeSheetUsers),
            "xml_parser": None,
            "xml_create": "users",
            "xml_read": "users",
            "xml_update": "users",
            "xml_delete": "users",
        },
    )
    __xml_tags: ClassVar[dict[str, str | dict[str, type]]] = {
        "xml_create_parent_tag": "sheets",
        "xml_create_tag": "cube-sheet",
        "xml_create_children": {},
        "xml_read_parent_tag": "sheets",
        "xml_read_tag": "cube-sheet",
        "xml_read_children": {
            "dimensions": CubeSheetDimension,
            "levels": CubeSheetLevels,
            "accounts": CubeSheetAccounts,
            "time": CubeSheetTime,
            "users": CubeSheetUsers,
        },
        "xml_update_parent_tag": "sheets",
        "xml_update_tag": "cube-sheet",
        "xml_update_children": {},
        "xml_delete_parent_tag": "sheets",
        "xml_delete_tag": "cube-sheet",
        "xml_delete_children": {},
    }
