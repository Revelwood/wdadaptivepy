"""wdadaptivepy service for Adaptive data."""

from csv import DictReader
from datetime import datetime
from io import StringIO
from typing import TYPE_CHECKING, Self
from xml.etree import ElementTree as ET

from wdadaptivepy.connectors.xml_api.xml_api import XMLApi
from wdadaptivepy.models.account import Account
from wdadaptivepy.models.base import bool_to_str_true_false
from wdadaptivepy.models.data import (
    AccountFilter,
    CurrencyFilter,
    DimensionValueFilter,
    ExportDataFilter,
    ExportDataFormat,
    ExportDataRules,
    LevelFilter,
    TimeFilter,
)
from wdadaptivepy.models.dimension import Dimension
from wdadaptivepy.models.dimension_value import DimensionValue
from wdadaptivepy.models.level import Level
from wdadaptivepy.models.time import Period, Stratum
from wdadaptivepy.models.version import Version

if TYPE_CHECKING:
    from collections.abc import Sequence


class DataQuery:
    def __init__(self) -> None:
        self._version_filter: Version | None = None
        self._account_filter: list[AccountFilter] = []
        self._time_filter: TimeFilter | None = None
        self._level_filter: list[LevelFilter] = []
        self._dimension_value_filter: list[DimensionValueFilter] = []
        self._returned_dimensions: list[Dimension] = []
        self._rules: ExportDataRules | None = None

    def _get_account_filter(
        self,
        accounts: Account | str | Sequence[Account | str],
        *,
        include_descendants: bool,
    ) -> AccountFilter:
        if isinstance(accounts, Account):
            account_search = accounts
        elif isinstance(accounts, str):
            account_search = Account(code=accounts)
        elif isinstance(accounts, Sequence):
            account_search = []
            for account in accounts:
                if isinstance(account, Account):
                    account_search.append(account)
                elif isinstance(account, str):
                    account_search.append(Account(code=account))
                else:
                    raise TypeError
        else:
            raise TypeError

        return AccountFilter(
            account=account_search,
            include_descendants=include_descendants,
        )

    def _get_time_filter(
        self,
        start_period: Period | str,
        end_period: Period | str | None = None,
        stratum: Stratum | str | None = None,
    ) -> TimeFilter:
        if isinstance(start_period, Period):
            start_period_search = start_period
        elif isinstance(start_period, str):
            start_period_search = Period(code=start_period)
        else:
            raise TypeError

        if end_period is None or isinstance(end_period, Period):
            end_period_search = end_period
        elif isinstance(end_period, str):
            end_period_search = Period(code=end_period)
        else:
            raise TypeError

        if stratum is None or isinstance(stratum, Stratum):
            stratum_filter = stratum
        elif isinstance(stratum, str):
            stratum_filter = Stratum(code=stratum)
        else:
            raise TypeError

        return TimeFilter(
            start=start_period_search,
            end=end_period_search,
            stratum=stratum_filter,
        )

    def _get_levels_filter(
        self, levels: Level | str | Sequence[Level | str]
    ) -> LevelFilter:
        if isinstance(levels, Level):
            levels_filter = LevelFilter(level=levels)
        elif isinstance(levels, str):
            levels_filter = LevelFilter(level=Level(code=levels))
        elif isinstance(levels, Sequence):
            level_search = []
            for level in levels:
                if isinstance(level, Level):
                    level_search.append(level)
                elif isinstance(level, str):
                    level_search.append(Level(code=level))
                else:
                    raise TypeError
            levels_filter = LevelFilter(level=level_search)
        else:
            raise TypeError

        return levels_filter

    def _get_dimension_values_filter(
        self,
        dimension_value: DimensionValue
        | str
        | Sequence[DimensionValue | str]
        | None = None,
        *,
        dimension: Dimension | str | None = None,
        direct_children: bool | None = None,
        uncategorized: bool | None = None,
        uncategorized_of_dimension: Dimension
        | str
        | bool
        | Sequence[Dimension | str]
        | None = None,
        direct_children_of_dimension: Dimension
        | str
        | bool
        | Sequence[Dimension | str]
        | None = None,
    ) -> DimensionValueFilter:
        if isinstance(dimension_values, DimensionValue):
            dimension_values_filter = DimensionValueFilter(
                dimension_value=dimension_values
            )
        elif isinstance(dimension_values, str):
            dimension_values_filter = Di
        elif isinstance(dimension_values, Sequence):
            dimension_values_search = []
            for dimension_value in dimension_values:
                if isinstance(dimension_value, DimensionValue):
                    dimension_values_search.append(dimension_value)
                else:
                    raise TypeError
            dimension_values_filter = DimensionValueFilter(
                dimension_value=dimension_values_search,
            )
        else:
            raise TypeError

        return dimension_values_filter

    def _generate_xml(self) -> ET.Element:
        if self._version_filter is None:
            raise ValueError
        if self._version_filter.name is None:
            raise ValueError

        if not self._account_filter:
            raise ValueError

        if not self._time_filter:
            raise ValueError

        data_filter = ExportDataFilter(
            accounts=self._account_filter,
            time=self._time_filter,
            levels=self._level_filter,
            dimension_values=self._dimension_value_filter,
        )

        payload: list[ET.Element] = []

        version_element = ET.Element(
            "version",
            attrib={"name": self._version_filter.name},
        )

        payload.append(version_element)

        if self._data_format:
            format_element = data_format.to_xml_element()
            payload.append(format_element)

        filter_element = data_filter.to_xml_element()
        payload.append(filter_element)

        if self._returned_dimensions:
            dimensions_element = ET.Element("dimensions")
            for dimension in self._returned_dimensions:
                dimension_element = self._create_dimension_element(dimension)
                dimensions_element.append(dimension_element)
            payload.append(dimensions_element)

        if self.rules is not None:
            rules_element = rules.to_xml_element()
            payload.append(rules_element)
        return payload

    def set_version_filter(self, version: Version | str) -> Self:
        if self._version_filter is not None:
            raise ValueError
        if isinstance(version, Version):
            if version.name is None or version.name == "":
                raise ValueError
            self._version_filter = version
        elif isinstance(version, str):
            self._version_filter = Version(name=version)
        else:
            raise TypeError

        return self

    def add_account_filter(
        self,
        account: Account | str | Sequence[Account | str],
        *,
        include_descendants: bool = True,
    ) -> Self:
        self._account_filter.append(
            self._get_account_filter(
                accounts=account,
                include_descendants=include_descendants,
            )
        )
        return self

    def set_time_filter(
        self,
        start_period: Period | str,
        end_period: Period | str | None = None,
        stratum: Stratum | str | None = None,
    ) -> Self:
        if self._time_filter is not None:
            raise ValueError

        self._get_time_filter(
            start_period=start_period,
            end_period=end_period,
            stratum=stratum,
        )
        return self

    def add_level_filter(self, level: Level | str | Sequence[Level | str]) -> Self:
        self._level_filter.append(self._get_levels_filter(levels=level))
        return self

    def add_dimension_value_filter(
        self,
        dimension_value: DimensionValue
        | str
        | Sequence[DimensionValue | str]
        | None = None,
        *,
        dimension: Dimension | str | None = None,
        direct_children: bool | None = None,
        uncategorized: bool | None = None,
        uncategorized_of_dimension: Dimension
        | str
        | bool
        | Sequence[Dimension | str]
        | None = None,
        direct_children_of_dimension: Dimension
        | str
        | bool
        | Sequence[Dimension | str]
        | None = None,
    ) -> Self:
        self._dimension_value_filter.append(
            self._get_dimension_values_filter(dimension_values=dimension_value)
        )
        return self

    def get_data(
        self,
    ) -> list[dict[str, str | int | float]]:
        payload = self._generate_xml()

        response = self.__xml_api.make_xml_request(
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

    def get_temp(
        self,
    ) -> None:
        if self._version_filter is None:
            raise ValueError

        if not self._account_filter:
            raise ValueError

        if not self._time_filter:
            raise ValueError

        data_filter = ExportDataFilter(
            accounts=self._account_filter,
            time=self._time_filter,
            levels=self._level_filter,
            dimension_values=self._dimension_value_filter,
        )

        dimensions_in_results = self._get_returned_dimensions(
            dimension_values_filter=dimension_values_filter,
            returned_dimensions=returned_dimensions,
        )

        unsigned_data = DataService().get_data(
            version=search_version,
            data_filter=data_filter,
            dimensions=dimensions_in_results,
        )

         if self.sign.debit_credit == True:
             accounts = self.get_accounts()


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
        self.__xml_api = xml_api
        self.ExportDataAccountsFilter = AccountFilter
        self.ExportDataCurrencyFilter = CurrencyFilter
        self.ExportDataDimensionValueFilter = DimensionValueFilter
        self.ExportDataFilter = ExportDataFilter
        self.ExportDataFormat = ExportDataFormat
        self.ExportDataRules = ExportDataRules
        self.ExportDataLevelFilter = LevelFilter
        self.ExportDataTimeFilter = TimeFilter

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

        response = self.__xml_api.make_xml_request(
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

        response = self.__xml_api.make_xml_request(
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
