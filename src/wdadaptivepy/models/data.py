"""wdadaptivepy model for Adaptive data."""

from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import TypeVar
from xml.etree import ElementTree as ET

from wdadaptivepy.models.account import Account
from wdadaptivepy.models.base import bool_to_str_true_false, int_to_str, str_to_str
from wdadaptivepy.models.dimension import Dimension
from wdadaptivepy.models.dimension_value import DimensionValue
from wdadaptivepy.models.level import Level
from wdadaptivepy.models.time import Period, Stratum

T = TypeVar("T")


def is_none_or_has_code(value: T | Sequence[T]) -> None:
    """Validate that a value is None or has a code.

    Args:
        value: Value to check if None or has a code

    """
    if value is None:
        return
    has_code(value)


def has_code(value: T | Sequence[T]) -> None:
    """Validate that a value has a code.

    Args:
        value: Value to validate has a code

    Raises:
        KeyError: Missing key
        ValueError: Unexpected value

    """
    if isinstance(value, Sequence):
        for item in value:
            has_code(item)
    if not hasattr(value, "code"):
        error_message = "Filter value missing code"
        raise KeyError(error_message)
    code = getattr(value, "code", None)
    if code in [None, ""]:
        error_message = "Filter value must have a code"
        raise ValueError(error_message)


def is_none_or_has_name(value: T | Sequence[T]) -> None:
    """Validate that a value is None or has a name.

    Args:
        value: Value to check if None or has a name

    """
    if value is None:
        return
    has_name(value)


def has_name(value: T | Sequence[T]) -> None:
    """Validate that a value has a name.

    Args:
        value: Value to validate has a name

    Raises:
        KeyError: Missing key
        ValueError: Unexpected value

    """
    if isinstance(value, Sequence):
        for item in value:
            has_code(item)
    if not hasattr(value, "name"):
        error_message = "Filter value missing code"
        raise KeyError(error_message)
    code = getattr(value, "code", None)
    if code in [None, ""]:
        error_message = "Filter value must have a code"
        raise ValueError(error_message)


def is_none_or_has_code_and_name(value: T | Sequence[T]) -> None:
    """Validate that a value is None or has a name and a code.

    Args:
        value: Value to validate isnone or has a name or a code

    """
    if value is None:
        return
    has_code_and_name(value)


def has_code_and_name(value: T | Sequence[T]) -> None:
    """Validate that a value has a code and a name.

    Args:
        value: Value to validate has a code and a name

    """
    has_code(value)
    has_name(value)


def is_none_or_is_bool(value: T | Sequence[T]) -> None:
    """Validate that a value is None or a boolean.

    Args:
        value: Value to validate is None or a boolean

    """
    if value is None:
        return
    is_bool(value)


def is_bool(value: T | Sequence[T]) -> None:
    """Validate that a value is boolean.

    Args:
        value: Value to validate is boolean

    Raises:
        TypeError: Unexpected type

    """
    if isinstance(value, Sequence):
        for item in value:
            is_bool(item)
    if not isinstance(value, bool):
        error_message = "Filter value must be a bool"
        raise TypeError(error_message)


def is_none_or_is_string(value: T | Sequence[T]) -> None:
    """Validate that a value is None or a string.

    Args:
        value: Value to validate is None or a string

    """
    if value is None:
        return
    is_string(value)


def is_string(value: T | Sequence[T]) -> None:
    """Validate that a value is a string.

    Args:
        value: Value to validate is a string

    Raises:
        TypeError: Unexpected type

    """
    if isinstance(value, Sequence):
        for item in value:
            is_string(item)
    if not isinstance(value, str):
        error_message = "Filter value must be a string"
        raise TypeError(error_message)


@dataclass
class AccountFilter:
    """Adaptive Account Filter.

    Attributes:
        account: Adaptive Account
        include_descendants: Adaptive Include Desccendants

    """

    account: Account | Sequence[Account] = field(metadata={"validator": has_code})
    include_descendants: bool = field(default=False, metadata={"validator": is_bool})


@dataclass
class LevelFilter:
    """Adaptive Level Filter.

    Attributes:
        level: Adaptive Level
        is_rollup: Adaptive Is Rollup
        include_descendants: Adaptive Include Descendants

    """

    level: Level | Sequence[Level] = field(metadata={"validator": has_code_and_name})
    is_rollup: bool = field(default=False, metadata={"validator": is_bool})
    include_descendants: bool = field(default=False, metadata={"validator": is_bool})


@dataclass
class TimeFilter:
    """Adaptive Time Filter.

    Attributes:
        start: Adaptive Start
        end: Adaptive End
        stratum: Adaptive Stratum

    """

    start: Period = field(metadata={"validator": has_code})
    end: Period = field(metadata={"validator": has_code})
    stratum: Stratum | None = field(
        default=None,
        metadata={"validator": is_none_or_has_code},
    )


@dataclass
class DimensionValueFilter:
    """Adaptive Dimension Value Filter.

    Attributes:
        dimension_value: Adaptive Dimension Value
        direct_children: Adaptive Direct Children
        uncategorized: Adaptive Uncategorized
        uncategorized_of_dimension: Adaptive Uncategorized of Dimension
        direct_children_of_dimension: Adaptive Directchildren of Dimension

    """

    dimension_value: DimensionValue | Sequence[DimensionValue] | None = field(
        metadata={"validator": is_none_or_has_code}, default=None
    )
    direct_children: bool | None = field(
        metadata={"validator": is_none_or_is_bool}, default=None
    )
    uncategorized: bool | None = field(
        metadata={"validator": is_none_or_is_bool}, default=None
    )
    uncategorized_of_dimension: Dimension | Sequence[Dimension] | None = None
    direct_children_of_dimension: bool | None = field(
        metadata={"validator": is_none_or_is_bool}, default=None
    )


@dataclass
class CurrencyFilter:
    """Adaptive Currency Filter.

    Attributes:
        use_corporate: Adaptive Use Corporate
        use_local: Adaptive Use Local
        override: Adaptive Override

    """

    use_corporate: bool | None = field(
        default=None,
        metadata={"validator": is_none_or_is_bool},
    )
    use_local: bool | None = field(
        default=None,
        metadata={"validator": is_none_or_is_bool},
    )
    override: str | None = field(
        default=None,
        metadata={"validator": is_none_or_is_string},
    )

    def to_xml_element(self) -> ET.Element:
        """Convert Currency Filter to XML Element.

        Returns:
            XML Element

        Raises:
            ValueError: Unexpected value

        """
        currency_element = ET.Element("currency")

        use_corporate = bool_to_str_true_false(self.use_corporate)
        use_local = bool_to_str_true_false(self.use_local)
        override = str_to_str(self.override)
        property_count = sum(
            1 for attr in (use_corporate, use_local, override) if attr is not None
        )
        if property_count != 1:
            error_message = "Expected exactly least one currency property"
            raise ValueError(error_message)

        if use_corporate is not None:
            currency_element.attrib["useCorporate"] = use_corporate

        if use_local is not None:
            currency_element.attrib["useLocal"] = use_local

        if override is not None:
            currency_element.attrib["override"] = override

        return currency_element


@dataclass
class ExportDataRules:
    """Adaptive Export Data Rules.

    Attributes:
        include_zero_rows: Adaptive Include Zero Rows
        include_rollup_accounts: Adaptive Include Rollup Accounts
        include_rollup_levels: ADaptive Include Rollup Levels
        mark_invalid_values: Adaptive Mark Invalid Values
        mark_blanks: Adaptive Mark Blanks
        time_rollups: Adaptive Time Rollups
        currency: Adaptive Currency

    """

    include_zero_rows: bool | None = field(
        metadata={"validator": is_none_or_is_bool},
    )
    include_rollup_accounts: bool | None = field(
        metadata={"validator": is_none_or_is_bool},
    )
    include_rollup_levels: bool | None = field(
        metadata={"validator": is_none_or_is_bool},
    )
    mark_invalid_values: bool | None = field(
        metadata={"validator": is_none_or_is_bool},
    )
    mark_blanks: bool | None = field(metadata={"validator": is_none_or_is_bool})
    time_rollups: bool | None = field(metadata={"validator": is_none_or_is_bool})
    currency: CurrencyFilter | None = field(default=None)

    def to_xml_element(self) -> ET.Element:
        """Convert ExportDataRules to XML Element.

        Returns:
            XML Element

        """
        rules_element = ET.Element("rules")

        include_zero_rows = bool_to_str_true_false(self.include_zero_rows)
        if include_zero_rows is not None:
            rules_element.attrib["includeZeroRows"] = include_zero_rows

        include_rollup_accounts = bool_to_str_true_false(self.include_rollup_accounts)
        if include_rollup_accounts is not None:
            rules_element.attrib["includeRollupAccounts"] = include_rollup_accounts

        include_rollup_levels = bool_to_str_true_false(self.include_rollup_levels)
        if include_rollup_levels is not None:
            rules_element.attrib["includeRollupLevels"] = include_rollup_levels

        mark_invalid_values = bool_to_str_true_false(self.mark_invalid_values)
        if mark_invalid_values is not None:
            rules_element.attrib["markInvalidValues"] = mark_invalid_values

        mark_blanks = bool_to_str_true_false(self.mark_blanks)
        if mark_blanks is not None:
            rules_element.attrib["markBlanks"] = mark_blanks

        time_rollups = bool_to_str_true_false(self.time_rollups)
        if time_rollups is not None:
            rules_element.attrib["timeRollups"] = time_rollups

        if self.currency is not None:
            rules_element.append(self.currency.to_xml_element())

        return rules_element


@dataclass
class ExportDataFilter:
    """Adaptive Export Data Filter.

    Attributes:
        accounts: Adaptive Accounts
        time: Adaptive Time
        levels: Adaptive Levels
        dimension_values: Adaptive Dimension Values

    """

    accounts: AccountFilter | Sequence[AccountFilter]
    time: TimeFilter
    levels: LevelFilter | Sequence[LevelFilter] | None = field(
        default=None,
    )
    dimension_values: DimensionValueFilter | Sequence[DimensionValueFilter] | None = (
        field(default=None)
    )

    def to_xml_element(self) -> ET.Element:  # NOQA: PLR0912, PLR0915
        """Convert ExportDataFilter to XML Element.

        Returns:
            XML Element

        Raises:
            ValueError: Unexpected value

        """
        filters_element = ET.Element("filters")

        accounts_element = ET.Element("accounts")
        if isinstance(self.accounts, Sequence):
            for account_filter in self.accounts:
                include_descendants = bool_to_str_true_false(
                    account_filter.include_descendants,
                )
                if include_descendants is None:
                    error_message = "Expected include_descendants value"
                    raise ValueError(error_message)
                if isinstance(account_filter.account, Sequence):
                    for account in account_filter.account:
                        code = str_to_str(account.code)
                        if code is None:
                            error_message = "Expected code value"
                            raise ValueError(error_message)
                        is_assumption = bool_to_str_true_false(account.is_assumption)
                        if is_assumption is None:
                            error_message = "Expected is_assumption value"
                            raise ValueError(error_message)
                        account_element = ET.Element(
                            "account",
                            attrib={
                                "code": code,
                                "isAssumption": is_assumption,
                                "includeDescendants": include_descendants,
                            },
                        )
                        accounts_element.append(account_element)
                else:
                    account = account_filter.account
                    code = str_to_str(account.code)
                    if code is None:
                        error_message = "Expected code value"
                        raise ValueError(error_message)
                    is_assumption = bool_to_str_true_false(account.is_assumption)
                    if is_assumption is None:
                        error_message = "Expected is_assumption value"
                        raise ValueError(error_message)
                    account_element = ET.Element(
                        "account",
                        attrib={
                            "code": code,
                            "isAssumption": is_assumption,
                            "includeDescendants": include_descendants,
                        },
                    )
                    accounts_element.append(account_element)
        else:
            account_filter = self.accounts
            include_descendants = bool_to_str_true_false(
                account_filter.include_descendants,
            )
            if include_descendants is None:
                error_message = "Expected include_descendants value"
                raise ValueError(error_message)
            if isinstance(account_filter.account, Sequence):
                for account in account_filter.account:
                    code = str_to_str(account.code)
                    if code is None:
                        error_message = "Expected code value"
                        raise ValueError(error_message)
                    is_assumption = bool_to_str_true_false(account.is_assumption)
                    if is_assumption is None:
                        error_message = "Expected is_assumption value"
                        raise ValueError(error_message)
                    account_element = ET.Element(
                        "account",
                        attrib={
                            "code": code,
                            "isAssumption": is_assumption,
                            "includeDescendants": include_descendants,
                        },
                    )
                    accounts_element.append(account_element)
            else:
                account = account_filter.account
                code = str_to_str(account.code)
                if code is None:
                    error_message = "Expected code value"
                    raise ValueError(error_message)
                is_assumption = bool_to_str_true_false(account.is_assumption)
                if is_assumption is None:
                    error_message = "Expected is_assumption value"
                    raise ValueError(error_message)
                account_element = ET.Element(
                    "account",
                    attrib={
                        "code": code,
                        "isAssumption": is_assumption,
                        "includeDescendants": include_descendants,
                    },
                )
                accounts_element.append(account_element)
        filters_element.append(accounts_element)

        if self.levels is not None:
            levels_element = ET.Element("levels")
            if isinstance(self.levels, Sequence):
                for level_filter in self.levels:
                    is_rollup = bool_to_str_true_false(level_filter.is_rollup)
                    if is_rollup is None:
                        error_message = "Expected is_rollup value"
                        raise ValueError(error_message)
                    include_descendants = bool_to_str_true_false(
                        level_filter.include_descendants,
                    )
                    if include_descendants is None:
                        error_message = "Expected include_descendants value"
                        raise ValueError(error_message)
                    if isinstance(level_filter.level, Sequence):
                        for level in level_filter.level:
                            code = str_to_str(level.code)
                            if code is None:
                                error_message = "Expected code value"
                                raise ValueError(error_message)
                            level_element = ET.Element(
                                "level",
                                attrib={
                                    "code": code,
                                    "isRollup": is_rollup,
                                    "includeDescendants": include_descendants,
                                },
                            )
                            levels_element.append(level_element)
                    else:
                        level = level_filter.level
                        code = str_to_str(level.code)
                        if code is None:
                            error_message = "Expected code value"
                            raise ValueError(error_message)
                        level_element = ET.Element(
                            "level",
                            attrib={
                                "code": code,
                                "isRollup": is_rollup,
                                "includeDescendants": include_descendants,
                            },
                        )
                        levels_element.append(level_element)
            else:
                level_filter = self.levels
                is_rollup = bool_to_str_true_false(level_filter.is_rollup)
                if is_rollup is None:
                    error_message = "Expected is_rollup value"
                    raise ValueError(error_message)
                include_descendants = bool_to_str_true_false(
                    level_filter.include_descendants,
                )
                if include_descendants is None:
                    error_message = "Expected include_descendants value"
                    raise ValueError(error_message)
                if isinstance(level_filter.level, Sequence):
                    for level in level_filter.level:
                        code = str_to_str(level.code)
                        if code is None:
                            error_message = "Expected code value"
                            raise ValueError(error_message)
                        level_element = ET.Element(
                            "level",
                            attrib={
                                "code": code,
                                "isRollup": is_rollup,
                                "includeDescendants": include_descendants,
                            },
                        )
                        levels_element.append(level_element)
                else:
                    level = level_filter.level
                    code = str_to_str(level.code)
                    if code is None:
                        error_message = "Expected code value"
                        raise ValueError(error_message)
                    level_element = ET.Element(
                        "level",
                        attrib={
                            "code": code,
                            "isRollup": is_rollup,
                            "includeDescendants": include_descendants,
                        },
                    )
                    levels_element.append(level_element)
            filters_element.append(levels_element)

        start = str_to_str(self.time.start.code)
        if start is None:
            error_message = "Expected start value"
            raise ValueError(error_message)
        end = str_to_str(self.time.end.code)
        if end is None:
            error_message = "Expected end value"
            raise ValueError(error_message)

        if self.dimension_values is not None:
            dimension_values_element = ET.Element("dimensionValues")
            if isinstance(self.dimension_values, Sequence):
                for dimension_value_filter in self.dimension_values:
                    if isinstance(dimension_value_filter.dimension_value, Sequence):
                        for dimension_value in dimension_value_filter.dimension_value:
                            dimension_value_element = ET.Element(
                                "dimensionValue", attrib={"id": str(dimension_value.id)}
                            )
                            dimension_values_element.append(dimension_value_element)
                    elif isinstance(
                        dimension_value_filter.uncategorized_of_dimension,
                        Sequence,
                    ):
                        for (
                            dimension
                        ) in dimension_value_filter.uncategorized_of_dimension:
                            dimension_value_element = ET.Element("dimensionValue")
                            dimension_name = str_to_str(dimension.name)
                            dimension_id = int_to_str(dimension.id)
                            if dimension_name is None and dimension_id is None:
                                error_message = (
                                    "One or more of dimension name or "
                                    "dimension id value expected"
                                )
                                raise ValueError(error_message)
                            if dimension_id is not None:
                                dimension_value_element.attrib[
                                    "uncategorizedOfDimension"
                                ] = dimension_id
                            elif dimension_name is not None:
                                dimension_value_element.attrib["uncategorized"] = (
                                    dimension_name
                                )
                            dimension_values_element.append(dimension_value_element)
                    elif dimension_value_filter.uncategorized_of_dimension is not None:
                        dimension = dimension_value_filter.uncategorized_of_dimension
                        dimension_value_element = ET.Element("dimensionValue")
                        dimension_name = str_to_str(dimension.name)
                        dimension_id = int_to_str(dimension.id)
                        if dimension_name is None and dimension_id is None:
                            error_message = (
                                "One or more of dimension name "
                                "or dimension id value expected"
                            )
                            raise ValueError(error_message)
                        if dimension_id is not None:
                            dimension_value_element.attrib[
                                "uncategorizedOfDimension"
                            ] = dimension_id
                        elif dimension_name is not None:
                            dimension_value_element.attrib["uncategorized"] = (
                                dimension_name
                            )
                        dimension_values_element.append(dimension_value_element)
            elif isinstance(self.dimension_values, DimensionValueFilter) and isinstance(
                self.dimension_values.dimension_value, Sequence
            ):
                for dimension_value in self.dimension_values.dimension_value:
                    dimension_value_element = ET.Element(
                        "dimensionValue",
                        attrib={"id": str(dimension_value.id)},
                    )
                    dimension_values_element.append(dimension_value_element)
            filters_element.append(dimension_values_element)

        time_span_element = ET.Element("timeSpan", attrib={"start": start, "end": end})
        if self.time.stratum is not None:
            stratum = str_to_str(self.time.stratum.code)
            if stratum is not None:
                time_span_element.attrib["stratum"] = stratum
        filters_element.append(time_span_element)

        return filters_element


@dataclass
class ExportDataFormat:
    """Adaptive Export Data Format.

    Attributes:
        use_internal_codes: Adaptive Use Internal Codes
        use_ids: Adaptive Use IDs
        include_unmapped_items: Adaptive Include Unmapped Items
        include_codes: Adaptive Include Codes
        include_names: Adaptive Include Names
        include_display_names: Adaptive Include Display Names
        display_name_enabled: Adaptive Display Name Enabled

    """

    use_internal_codes: bool = field(default=True, metadata={"validator": is_bool})
    use_ids: bool | None = field(
        default=False,
        metadata={"validator": is_none_or_is_bool},
    )
    include_unmapped_items: bool | None = field(
        default=True,
        metadata={"validator": is_none_or_is_bool},
    )
    include_codes: bool | None = field(
        default=True,
        metadata={"validator": is_none_or_is_bool},
    )
    include_names: bool | None = field(
        default=True,
        metadata={"validator": is_none_or_is_bool},
    )
    include_display_names: bool | None = field(
        default=False,
        metadata={"validator": is_none_or_is_bool},
    )
    display_name_enabled: bool | None = field(
        default=True,
        metadata={"validator": is_none_or_is_bool},
    )

    def to_xml_element(self) -> ET.Element:
        """Convert Export Data Format to XML Element.

        Returns:
            XML Element

        Raises:
            ValueError: Unexpected value

        """
        format_element = ET.Element("format")

        use_internal_codes = bool_to_str_true_false(self.use_internal_codes)
        if use_internal_codes is None:
            error_message = "Expected value for use_internal_codes"
            raise ValueError(error_message)
        format_element.attrib["useInternalCodes"] = use_internal_codes

        use_ids = bool_to_str_true_false(self.use_ids)
        if use_ids is not None:
            format_element.attrib["useIds"] = use_ids

        incudle_unmapped_items = bool_to_str_true_false(self.include_unmapped_items)
        if incudle_unmapped_items is not None:
            format_element.attrib["includeUnmappedItems"] = incudle_unmapped_items

        include_codes = bool_to_str_true_false(self.include_codes)
        if include_codes is not None:
            format_element.attrib["includeCodes"] = include_codes

        include_names = bool_to_str_true_false(self.include_names)
        if include_names is not None:
            format_element.attrib["includeNames"] = include_names

        include_display_names = bool_to_str_true_false(self.include_display_names)
        if include_display_names is not None:
            format_element.attrib["includeDisplayNames"] = include_display_names

        display_name_enabled = bool_to_str_true_false(self.display_name_enabled)
        if display_name_enabled is not None:
            format_element.attrib["displayNameEnabled"] = display_name_enabled

        return format_element
