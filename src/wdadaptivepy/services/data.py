"""wdadaptivepy service for Adaptive data."""

import sys
from collections.abc import Sequence
from csv import DictReader, reader
from datetime import datetime
from io import StringIO
from typing import TypeVar, cast
from xml.etree import ElementTree as ET

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

from wdadaptivepy.connectors.xml_api.xml_api import XMLApi
from wdadaptivepy.models.account import Account
from wdadaptivepy.models.data import (
    AccountFilter,
    CurrencyFilter,
    DimensionValueFilter,
    ExportDataFilter,
    ExportDataFormat,
    ExportDataRules,
    LevelFilter,
    TimeFilter,
    VersionFilter,
)
from wdadaptivepy.models.dimension import Dimension
from wdadaptivepy.models.dimension_value import DimensionValue
from wdadaptivepy.models.level import Level
from wdadaptivepy.models.time import Period, Stratum
from wdadaptivepy.models.version import Version
from wdadaptivepy.utils.parsers import bool_to_str_true_false

T = TypeVar("T")


class DataQuery:
    """Query builder for Adaptive's export_data API."""

    def __init__(self, xml_api: XMLApi) -> None:
        """Initialize DataQuery."""
        self._xml_api = xml_api
        self._version_filter = VersionFilter(version=None, is_default=None)
        self._account_filter: list[AccountFilter] = []
        self._time_filter: TimeFilter | None = None
        self._level_filter: list[LevelFilter] = []
        self._dimension_value_filter: list[DimensionValueFilter] = []
        self._returned_dimensions: list[Dimension] = []
        self._rules: ExportDataRules = ExportDataRules(
            include_zero_rows=False,
            include_rollup_accounts=False,
            include_rollup_levels=False,
            mark_invalid_values=False,
            mark_blanks=False,
            time_rollups=False,
            currency=CurrencyFilter(
                use_corporate=None,
                use_local=True,
                override=None,
            ),
        )

    def _get_flat_list_obj(
        self,
        obj: T | Sequence[T],
    ) -> list[T]:
        if isinstance(obj, (str, bytes)):
            return [cast("T", obj)]
        if isinstance(obj, Sequence):
            return list(obj)
        return [obj]

    def _get_version_obj(self, version: Version | str) -> Version:
        if isinstance(version, Version):
            if not version.name:
                raise ValueError
            return version
        if isinstance(version, str):
            return Version(name=version)
        raise TypeError

    def set_version_filter(
        self,
        version: Version | str | None = None,
        *,
        use_default: bool = False,
    ) -> Self:
        """Set the Version for export_data.

        Args:
            version: Version of the data query.
            use_default: Use the default Adaptive Version

        Returns:
            Modified DataQuery object.

        """
        if use_default is True:
            self._version_filter.version = None
            self._version_filter.is_default = True
        else:
            if version is None:
                raise ValueError
            self._version_filter.version = self._get_version_obj(version)
            self._version_filter.is_default = None

        return self

    @property
    def version_filter(self) -> VersionFilter:
        """Get details of the data query's Version.

        Returns:
            Version used by Data Query

        """
        return self._version_filter

    def _get_account_obj(self, account: Account | str) -> Account:
        if isinstance(account, Account):
            if not account.code:
                raise ValueError
            if account.is_assumption is None:
                raise ValueError
            account_obj = account
        elif isinstance(account, str):
            account_obj = Account(code=account, is_assumption=False)
        else:
            raise TypeError
        return account_obj

    def add_account_filter(
        self,
        accounts: Account | str | Sequence[Account | str],
        *,
        include_descendants: bool = True,
    ) -> Self:
        """Add an Account filter to the data query.

        Args:
            accounts: Accounts for the data query
            include_descendants: Include the accounts' descendants

        Returns:
            Modified DataQuery object.

        """
        all_accounts = self._get_flat_list_obj(accounts)

        for account in all_accounts:
            account_obj = self._get_account_obj(account)
            self._account_filter.append(
                AccountFilter(
                    account=account_obj,
                    include_descendants=include_descendants,
                )
            )
        return self

    def clear_account_filter(self) -> Self:
        """Clear all account filters for the data query.

        Returns:
            Modified DataQuery object.

        """
        self._account_filter = []
        return self

    @property
    def account_filter(self) -> list[AccountFilter]:
        """Get all account filters for data query.

        Returns:
            List of account filters for data query.

        """
        return self._account_filter

    def _get_period_obj(self, period: Period | str) -> Period:
        if isinstance(period, Period):
            if not period.code:
                raise ValueError
            return period
        if isinstance(period, str):
            return Period(code=period)
        raise TypeError

    def _get_stratum_obj(self, stratum: Stratum | str) -> Stratum:
        if isinstance(stratum, Stratum):
            if not stratum.code:
                raise ValueError
            return stratum
        if isinstance(stratum, str):
            return Stratum(code=stratum)
        raise TypeError

    def set_time_filter(
        self,
        start_period: Period | str,
        end_period: Period | str,
        stratum: Stratum | str | None = None,
    ) -> Self:
        """Set the Time filter for the data query.

        Args:
            start_period: Start Period of the Data Query
            end_period: End Period of the Data Query
            stratum: Stratum of the Query

        Returns:
            Modified DataQuery object.

        """
        start_period_obj = self._get_period_obj(start_period)
        end_period_obj = self._get_period_obj(end_period)

        stratum_obj = self._get_stratum_obj(stratum) if stratum is not None else None

        self._time_filter = TimeFilter(
            start=start_period_obj,
            end=end_period_obj,
            stratum=stratum_obj,
        )
        return self

    @property
    def time_filter(self) -> TimeFilter | None:
        """Get the Time filter of the data query.

        Returns:
            DataQuery's Time filter

        """
        return self._time_filter

    def _get_level_obj(self, level: Level | str) -> Level:
        if isinstance(level, Level):
            if not level.code:
                raise ValueError
            return level
        if isinstance(level, str):
            return Level(code=level)
        raise TypeError

    def add_level_filter(
        self,
        levels: Level | str | Sequence[Level | str],
        *,
        is_rollup: bool = False,
        include_descendants: bool = True,
    ) -> Self:
        """Add Level to the data query.

        Args:
            levels: Levels for the data query
            is_rollup: Flag to include only the data loaded to a Level rollup
            include_descendants: Include the level's descendants

        Returns:
            Modified DataQuery object.

        """
        all_levels = self._get_flat_list_obj(levels)

        for level in all_levels:
            level_obj = self._get_level_obj(level)
            self._level_filter.append(
                LevelFilter(
                    level=level_obj,
                    is_rollup=is_rollup,
                    include_descendants=include_descendants,
                )
            )
        return self

    @property
    def level_filter(self) -> list[LevelFilter]:
        """Get the data query's level filter.

        Returns:
            List of Level filters.

        """
        return self._level_filter

    def clear_level_filter(self) -> Self:
        """Clear the level filters of the data query.

        Returns:
            Modified DataQuery object.

        """
        self._level_filter = []
        return self

    def _get_dimension_obj(self, dimension: Dimension | str) -> Dimension:
        if isinstance(dimension, Dimension):
            if not dimension.name:
                raise ValueError
            return dimension
        if isinstance(dimension, str):
            return Dimension(name=dimension)
        raise TypeError

    def _get_dimension_value_obj(
        self, dimension_value: DimensionValue | str | int
    ) -> DimensionValue:
        if isinstance(dimension_value, DimensionValue):
            if not dimension_value.code and not dimension_value.id:
                raise ValueError
            return dimension_value
        if isinstance(dimension_value, str):
            return DimensionValue(code=dimension_value)
        if isinstance(dimension_value, int):
            return DimensionValue(id=dimension_value)
        raise TypeError

    def add_dimension_value_filter(
        self,
        dimension: Dimension | str,
        dimension_values: DimensionValue
        | str
        | int
        | Sequence[DimensionValue | str | int],
        *,
        direct_children: bool | None = None,
        uncategorized: bool | None = None,
    ) -> Self:
        """Add filters for Dimension Values.

        Args:
            dimension: Dimension for the Data Query
            dimension_values: Dimension Values for the Data Query
            direct_children: Include only direct children of the dimension values
            uncategorized: Include only the uncategorized of the dimension value

        Returns:
            Modified DataQuery object.

        """
        dimension_obj = self._get_dimension_obj(dimension)
        all_dimension_values = self._get_flat_list_obj(dimension_values)

        for dimension_value in all_dimension_values:
            dimension_value_obj = self._get_dimension_value_obj(dimension_value)
            self._dimension_value_filter.append(
                DimensionValueFilter(
                    dimension=dimension_obj,
                    dimension_value=dimension_value_obj,
                    direct_children=direct_children,
                    uncategorized=uncategorized,
                )
            )
        return self

    def add_uncategorized_dimension_filter(
        self,
        dimensions: Dimension | Sequence[Dimension],
    ) -> Self:
        """Add the dimension's uncategorized dimension value as a filter.

        Args:
            dimensions: Adaptive Dimension to include uncategorized value

        Returns:
            Modified DataQuery object.

        """
        all_dimensions = self._get_flat_list_obj(dimensions)

        for dimension in all_dimensions:
            dimension_obj = self._get_dimension_obj(dimension)
            if dimension_obj.id is None:
                raise ValueError
            self._dimension_value_filter.append(
                DimensionValueFilter(uncategorized_of_dimension=dimension_obj)
            )

        return self

    def add_direct_children_of_dimension_filter(
        self,
        dimensions: Dimension | Sequence[Dimension],
    ) -> Self:
        """Add the immediate children of a Dimension as a filter.

        Args:
            dimensions: Adaptive Dimension to include direct children

        Returns:
            Modified DataQuery object.

        """
        all_dimensions = self._get_flat_list_obj(dimensions)

        for dimension in all_dimensions:
            dimension_obj = self._get_dimension_obj(dimension)
            if dimension_obj.id is None:
                raise ValueError
            self._dimension_value_filter.append(
                DimensionValueFilter(
                    direct_children_of_dimension=dimension_obj,
                )
            )

        return self

    @property
    def dimension_value_filter(self) -> list[DimensionValueFilter]:
        """Get the dimension value filter of the data query.

        Returns:
            Dimension Value Filter

        """
        return self._dimension_value_filter

    def clear_dimension_value_filter(self) -> Self:
        """Clear the dimension value filter.

        Returns:
            Modified DataQuery object.

        """
        self._dimension_value_filter = []
        return self

    def add_returned_dimension(
        self, dimensions: Dimension | str | Sequence[Dimension | str]
    ) -> Self:
        """Add Dimension to include as a column in the returned data.

        Args:
            dimensions: Adaptive Dimension

        Returns:
            Modified DataQuery object.

        """
        all_dimensions = self._get_flat_list_obj(dimensions)

        for dimension in all_dimensions:
            dimension_obj = self._get_dimension_obj(dimension)
            self._returned_dimensions.append(dimension_obj)
        return self

    def clear_returned_dimension(self) -> Self:
        """Clear the Dimensions to include as a column in the returned data.

        Returns:
            Modified DataQuery object.

        """
        self._returned_dimensions = []
        return self

    @property
    def returned_dimensions(self) -> list[str]:
        """Get the DImensions to include as a column in the returned data.

        Returns:
            List of Dimension names

        """
        dimensions: list[str] = []
        for dimension_value_filter in self._dimension_value_filter:
            if (
                dimension_value_filter.dimension is None
                or not dimension_value_filter.dimension.name
            ):
                raise ValueError
            if dimension_value_filter.dimension.name not in dimensions:
                dimensions.append(
                    dimension_value_filter.dimension.name,
                )
        for dimension in self._returned_dimensions:
            if not dimension.name:
                raise ValueError
            if dimension.name not in dimensions:
                dimensions.append(dimension.name)
        return dimensions

    def include_zero_rows(self) -> Self:
        """Include rows with zero values in returned data.

        Returns:
            Modified DataQuery object.

        """
        self._rules.include_zero_rows = True
        return self

    def exclude_zero_rows(self) -> Self:
        """Exclude rows with zero values in returned data.

        Returns:
            Modified DataQuery object.

        """
        self._rules.include_zero_rows = False
        return self

    def include_rollup_accounts(self) -> Self:
        """Include accounts that are rollups in the returned data.

        Returns:
            Modified DataQuery object.

        """
        self._rules.include_rollup_accounts = True
        return self

    def exclude_rollup_accounts(self) -> Self:
        """Exclude accounts that are rollups in the returned data.

        Returns:
            Modified DataQuery object.

        """
        self._rules.include_rollup_accounts = False
        return self

    def include_rollup_levels(self) -> Self:
        """Include Levels that are rollups in the returned data.

        Returns:
            Modified DataQuery object.

        """
        self._rules.include_rollup_levels = True
        return self

    def exclude_rollup_levels(self) -> Self:
        """Exclude Levels that are rollups in the returned data.

        Returns:
            Modified DataQuery object.

        """
        self._rules.include_rollup_levels = False
        return self

    def mark_invalid_values(self) -> Self:
        """Mark values that are invalid with a "I".

        Returns:
            Modified DataQuery object.

        """
        self._rules.mark_invalid_values = True
        return self

    def unmark_invalid_values(self) -> Self:
        """Do not mark values that are invalid.

        Returns:
            Modified DataQuery object.

        """
        self._rules.mark_invalid_values = False
        return self

    def mark_blanks(self) -> Self:
        """Mark blank values with a "B".

        Returns:
            Modified DataQuery object.

        """
        self._rules.mark_blanks = True
        return self

    def unmark_blanks(self) -> Self:
        """Do not mark values that are blank.

        Returns:
            Modified DataQuery object.

        """
        self._rules.mark_blanks = False
        return self

    def include_time_rollups(self) -> Self:
        """Include time rollups in returned data.

        Returns:
            Modified DataQuery object.

        """
        self._rules.time_rollups = True
        return self

    def exclude_time_rollups(self) -> Self:
        """Exclude time rollups in returned data.

        Returns:
            Modified DataQuery object.

        """
        self._rules.time_rollups = False
        return self

    def aggregate_time_periods(self) -> Self:
        """Aggregate all requested periods into a single period column.

        Returns:
            Modified DataQuery object.

        """
        self._rules.time_rollups = "single"
        return self

    def use_corporate_currency(self) -> Self:
        """Use the Top Level's Currency for all returned data.

        Returns:
            Modified DataQuery object.

        """
        self._rules.currency.use_corporate = True
        self._rules.currency.use_local = None
        self._rules.currency.override = None
        return self

    def use_local_currency(self) -> Self:
        """Use each Level's corresponding currency for all returned data.

        Returns:
            Modified DataQuery object.

        """
        self._rules.currency.use_corporate = None
        self._rules.currency.use_local = True
        self._rules.currency.override = None
        return self

    def use_override_currency(self, currency: str) -> Self:
        """Use a specific currency for all returned data.

        Args:
            currency: Currency to use for all returned data

        Returns:
            Modified DataQuery object.

        """
        self._rules.currency.use_corporate = None
        self._rules.currency.use_local = None
        self._rules.currency.override = currency
        return self

    def _validate_version_filter(self) -> None:
        if self._version_filter.is_default and self._version_filter.version is not None:
            raise ValueError

        if self._version_filter.version:
            if self._version_filter.is_default is not None:
                raise ValueError
            if not self._version_filter.version.name:
                raise ValueError

    def _validate_account_filter(self) -> None:
        if not self._account_filter:
            raise ValueError
        for account_filter in self._account_filter:
            if not account_filter.account:
                raise ValueError
            if not account_filter.account.code:
                raise ValueError
            if account_filter.account.is_assumption is None:
                raise ValueError

    def _validate_time_filter(self) -> None:
        if not self._time_filter:
            raise ValueError
        if not self._time_filter.start.code:
            raise ValueError
        if not self._time_filter.end.code:
            raise ValueError

    def _validate_dimension_value_filter(self) -> None:
        for dvf in self._dimension_value_filter:
            if dvf.dimension is None:
                raise ValueError
            if not dvf.dimension.name:
                raise ValueError

            has_dimension_value = dvf.dimension_value is not None and (
                dvf.dimension_value.code is not None
                or dvf.dimension_value.id is not None
            )
            has_direct_children = (
                dvf.direct_children_of_dimension is not None
                and dvf.direct_children_of_dimension.id is not None
            )
            has_uncategorized = (
                dvf.uncategorized_of_dimension is not None
                and dvf.uncategorized_of_dimension.id is not None
            )
            if dvf.dimension_value is not None and not has_dimension_value:
                raise ValueError
            if dvf.direct_children_of_dimension is not None and not has_direct_children:
                raise ValueError
            if dvf.uncategorized_of_dimension is not None and not has_uncategorized:
                raise ValueError

            if not any([has_dimension_value, has_direct_children, has_uncategorized]):
                raise ValueError

    def _validate_returned_dimensions(self) -> None:
        for dimension in self._returned_dimensions:
            if not dimension.name:
                raise ValueError
        for dimension_value_filter in self._dimension_value_filter:
            if (
                not dimension_value_filter.dimension
                or not dimension_value_filter.dimension.name
            ):
                raise ValueError

    def _validate_rules(self) -> None:
        currency = self._rules.currency

        defined_rules = (
            currency.use_corporate is not None,
            currency.use_local is not None,
            currency.override is not None,
        )
        if sum(defined_rules) != 1:
            raise ValueError

        active_rules = (
            self._rules.currency.use_corporate is True,
            self._rules.currency.use_local is True,
            bool(self._rules.currency.override),
        )
        if sum(active_rules) != 1:
            raise ValueError

    def _validate_data_query(self) -> None:
        self._validate_version_filter()
        self._validate_account_filter()
        self._validate_time_filter()
        self._validate_dimension_value_filter()
        self._validate_returned_dimensions()
        self._validate_rules()

    def _generate_xml(self) -> list[ET.Element]:
        self._validate_data_query()

        payload: list[ET.Element] = []

        payload.append(
            ExportDataFormat(
                use_internal_codes=True,
                use_ids=False,
                include_unmapped_items=False,
                include_codes=True,
                include_names=True,
                include_display_names=False,
                display_name_enabled=True,
            ).to_xml_element()
        )

        payload.append(self._version_filter.to_xml_element())

        if not self._time_filter:
            raise ValueError
        payload.append(
            ExportDataFilter(
                accounts=self._account_filter,
                time=self._time_filter,
                levels=self._level_filter,
                dimension_values=self._dimension_value_filter,
            ).to_xml_element()
        )

        if self.returned_dimensions:
            dimensions_element = ET.Element("dimensions")
            for dimension in self.returned_dimensions:
                dimensions_element.append(
                    ET.Element("dimension", attrib={"name": dimension})
                )
            payload.append(dimensions_element)

        payload.append(self._rules.to_xml_element())

        return payload

    def _parse_response(
        self,
        response: ET.Element,
    ) -> list[dict[str, str | float | int | None]]:
        """Parse data from XML.

        It reads like a table of contents for the parsing pipeline.

        """
        expected_count, csv_text = self._extract_payload(response)
        if not csv_text:
            return []

        headers, raw_rows = self._read_csv(csv_text, expected_count)
        if not headers or not raw_rows:
            return []

        base_cols, period_cols = self._categorize_columns(headers)
        return self._unpivot_data(raw_rows, base_cols, period_cols)

    def _extract_payload(self, response: ET.Element) -> tuple[int, str | None]:
        """Extract metadata and raw CSV text from the XML."""
        expected_count = -1
        status = response.find("status")
        if status is not None and "rowCountSent" in status.attrib:
            expected_count = int(status.attrib["rowCountSent"])

        data_element = response.find("output")
        csv_text = data_element.text if data_element is not None else None

        return expected_count, csv_text

    def _read_csv(
        self, csv_text: str, expected_count: int
    ) -> tuple[list[str], list[list[str]]]:
        """Parse CSV text into lists and validates row counts."""
        csv_reader = reader(StringIO(csv_text.lstrip("\n")), lineterminator="\n")

        try:
            headers = next(csv_reader)
        except StopIteration:
            return [], []

        raw_rows = list(csv_reader)

        if expected_count > -1 and len(raw_rows) != expected_count:
            raise RuntimeError

        return headers, raw_rows

    def _categorize_columns(
        self, headers: Sequence[str]
    ) -> tuple[list[tuple[int, str]], list[tuple[int, str]]]:
        """Separates column indices into 'base' and 'period' categories."""
        base_cols: list[tuple[int, str]] = []
        period_cols: list[tuple[int, str]] = []

        for idx, name in enumerate(headers):
            if name.endswith((" Name", " Code")):
                base_cols.append((idx, name))
            else:
                period_cols.append((idx, name))

        return base_cols, period_cols

    def _cast_amount(self, raw_amount: str) -> int | float | None:
        """Cast string amount to number."""
        if raw_amount == "B":
            return None
        try:
            return int(raw_amount)
        except ValueError:
            return float(raw_amount)

    def _unpivot_data(
        self,
        raw_rows: list[list[str]],
        base_cols: list[tuple[int, str]],
        period_cols: list[tuple[int, str]],
    ) -> list[dict[str, str | float | int | None]]:
        """Melts wide data into long format using high-speed integer indexing."""
        parsed_data: list[dict[str, str | float | int | None]] = []

        for row in raw_rows:
            base_row: dict[str, str | float | int | None] = {
                name: row[idx] for idx, name in base_cols
            }
            for idx, period_name in period_cols:
                new_row = base_row.copy()
                new_row["Period Code"] = period_name
                new_row["Amount"] = self._cast_amount(row[idx])
                parsed_data.append(new_row)

        return parsed_data

    def get_data(self) -> list[dict[str, str | int | float | None]]:
        """Retrieve data from Adaptive.

        Returns:
            Data from Adaptive

        """
        payload = self._generate_xml()

        if not payload:
            raise ValueError
        response = self._xml_api.make_xml_request(
            method="exportData",
            payload=payload,
            stream=True,
        )

        return self._parse_response(response)


class DataService:
    """wdadaptivepy Service for Data.

    Attributes:
        ExportDataAccountsFilter: Adaptive Accounts Filter
        ExportDataCurrencyFilter: Adaptive Currency Filter
        ExportDataDimensionValueFilter: Adaptive Dimension Value Filter
        ExportDataFilter: Adaptive Data Filter
        ExportDataFormat: Adaptive Data Format
        ExportDataRules: Adaptive  Rules
        ExportDataLevelFilter: Adaptive Level Filter
        ExportDataTimeFilter: Adaptive Time Filter

    """

    def __init__(self, xml_api: XMLApi) -> None:
        """Initialize DataService.

        Args:
            xml_api: wdadaptivepy XMLApi

        """
        self._xml_api = xml_api
        self.ExportDataAccountsFilter = AccountFilter
        self.ExportDataCurrencyFilter = CurrencyFilter
        self.ExportDataDimensionValueFilter = DimensionValueFilter
        self.ExportDataFilter = ExportDataFilter
        self.ExportDataFormat = ExportDataFormat
        self.ExportDataRules = ExportDataRules
        self.ExportDataLevelFilter = LevelFilter
        self.ExportDataTimeFilter = TimeFilter

    def query_data(self) -> DataQuery:
        """Start a data query to retrieve data from Adaptive.

        Returns:
            DataQuery object

        """
        return DataQuery(xml_api=self._xml_api)

    def _create_dimension_element(self, dimension: Dimension) -> ET.Element:
        if dimension.name is None:
            error_message = "Dimension name cannot be None"
            raise ValueError(error_message)
        return ET.Element("dimension", attrib={"name": dimension.name})

    def get_data(  # NOQA: PLR0915 PLR0912 C901
        self,
        version: Version,
        data_filter: ExportDataFilter,
        data_format: ExportDataFormat | None = None,
        dimensions: Dimension | list[Dimension] | None = None,
        rules: ExportDataRules | None = None,
    ) -> list[dict[str, str | int | float]]:
        """Retrieve Data from Adaptive.

        Args:
            version: Adaptive Version
            data_filter: Adaptive Filter
            data_format: Adaptive Format
            dimensions: Adaptive Dimensions
            rules: Adaptive Rules

        Returns:
            List of rows of data

        Raises:
            ValueError: Unexpected value
            RuntimeError: Unexpected error

        """
        if data_format is None:
            data_format = ExportDataFormat()

        payload: list[ET.Element] = []

        if version.name is None:
            error_message = "Expected Version name value"
            raise ValueError(error_message)
        version_element = ET.Element("version", attrib={"name": version.name})
        payload.append(version_element)

        format_element = data_format.to_xml_element()
        payload.append(format_element)

        filter_element = data_filter.to_xml_element()
        payload.append(filter_element)

        if dimensions is not None:
            dimensions_element = ET.Element("dimensions")
            if isinstance(dimensions, list):
                for dimension in dimensions:
                    dimension_element = self._create_dimension_element(dimension)
                    dimensions_element.append(dimension_element)
            else:
                dimension_element = self._create_dimension_element(dimensions)
                dimensions_element.append(dimension_element)
            payload.append(dimensions_element)
        if rules is not None:
            rules_element = rules.to_xml_element()
            payload.append(rules_element)

        response = self._xml_api.make_xml_request(
            method="exportData",
            payload=payload,
        )

        received_row_count = -1
        status_element = response.find("status")
        if status_element:
            row_count_sent = status_element.attrib["rowCountSent"]
            if row_count_sent:
                received_row_count = int(row_count_sent)
        data_element = response.find("output")
        data: list[dict[str, str | int | float]] = []
        column_headers: Sequence[str] | None = None
        if data_element is not None and data_element.text is not None:
            rows = StringIO(data_element.text.lstrip("\n"))
            csv_reader = DictReader(rows, lineterminator="\n")
            column_headers = csv_reader.fieldnames
            data = list(csv_reader)
        if received_row_count > -1 and received_row_count != len(data):
            error_message = (
                "Inconsistent row counts: expected "
                f"{received_row_count}, got {len(data)}"
            )
            raise RuntimeError(error_message)

        if column_headers is not None:
            period_columns = [
                period
                for period in column_headers
                if not (period.endswith((" Name", " Code")))
            ]
            parsed_data: list[dict[str, str | int | float]] = []
            for data_row in data:
                for period in period_columns:
                    row: dict[str, str | int | float] = {}
                    for column in column_headers:
                        if column in period_columns:
                            break
                        row[column] = data_row[column]
                    row["Period Code"] = period
                    try:
                        row["Amount"] = int(data_row[period])
                    except ValueError:
                        row["Amount"] = float(data_row[period])

                    parsed_data.append(row)
            return parsed_data

        return data

    def from_modeled_sheet(  # NOQA: PLR0913
        self,
        version_name: str,
        sheet_name: str,
        *,
        is_assumption_sheet: bool = False,
        include_all_columns: bool = True,
        get_all_rows: bool = True,
        use_numeric_ids: bool = False,
        display_name_enabled: bool = True,
        include_codes: bool = False,
        include_names: bool = False,
        include_display_names: bool = False,
        use_account_precision: bool = False,
        use_actual_value: bool = False,
    ) -> list[dict[str, str | int | float | bool | datetime]]:
        """Retrieve Adaptive Data from a Modeled Sheet.

        Args:
            version_name: Adaptive Version Name
            sheet_name: Adaptive Sheet Name
            is_assumption_sheet: Adaptive Is Assumption Sheet
            include_all_columns: Adaptive Include All Columns
            get_all_rows: Adaptive Get All Rows
            use_numeric_ids: Adaptive Use Numeric IDs
            display_name_enabled: Adaptive Display Name Enabled
            include_codes: Adaptive Include Codes
            include_names: Adaptive Include Names
            include_display_names: Adaptive Include Display Names
            use_account_precision: Adaptive Use Account Precision
            use_actual_value: Adaptive Use Actual Value

        Returns:
            List of rows of data

        """
        version_element = ET.Element("version", attrib={"name": version_name})
        modeled_sheet_element = ET.Element(
            "modeled-sheet",
            attrib={
                "name": sheet_name,
                "isGlobal": str(bool_to_str_true_false(is_assumption_sheet)),
                "includeAllColumns": str(bool_to_str_true_false(include_all_columns)),
                "isGetAllRows": str(bool_to_str_true_false(get_all_rows)),
                "useNumericIDs": str(bool_to_str_true_false(use_numeric_ids)),
                "diplsayNameEnabled": str(bool_to_str_true_false(display_name_enabled)),
                "includeCodes": str(bool_to_str_true_false(include_codes)),
                "includeNames": str(bool_to_str_true_false(include_names)),
                "includeDisplayNames": str(
                    bool_to_str_true_false(include_display_names),
                ),
                "useAccountPrecision": str(
                    bool_to_str_true_false(use_account_precision),
                ),
                "useActualValue": str(bool_to_str_true_false(use_actual_value)),
            },
        )

        response = self._xml_api.make_xml_request(
            method="exportConfigurableModelData",
            payload=[version_element, modeled_sheet_element],
        )
        data = response.find("output/data")
        sheet_data: list[dict[str, str | int | float | datetime]] = []
        if data is not None and data.text is not None:
            rows = StringIO(data.text.lstrip("\n"))
            csv_reader = DictReader(rows, lineterminator="\n")
            sheet_data = list(csv_reader)

        return sheet_data
