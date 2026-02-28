"""Test DataQuery's get_data's request's XML body."""

from collections.abc import Callable
from xml.etree import ElementTree as ET

import pytest

from wdadaptivepy.connectors.xml_api.xml_api import XMLApi
from wdadaptivepy.models.account import Account
from wdadaptivepy.models.time import Period, Stratum
from wdadaptivepy.models.version import Version
from wdadaptivepy.services.data import DataQuery


@pytest.fixture
def query() -> DataQuery:
    """Fixture for DataQuery.

    Returns:
        DataQuery

    """
    return DataQuery(XMLApi("", ""))


@pytest.mark.parametrize(
    ("query_config", "exception", "message"),
    [
        pytest.param(
            lambda q: q.set_time_filter("01/2026", "03/2026").add_account_filter(
                "Assets"
            ),
            ValueError,
            r"^$",
            id="missing_version_filter",
        ),
        pytest.param(
            lambda q: q.set_version_filter("Actuals").add_account_filter("Assets"),
            ValueError,
            r"^$",
            id="missing_time_filter",
        ),
        pytest.param(
            lambda q: q.set_version_filter("Actuals").set_time_filter(
                "01/2026", "03/2026"
            ),
            ValueError,
            r"^$",
            id="missing_account_filter",
        ),
    ],
)
def test_data_query_exceptions(
    query: DataQuery,
    query_config: Callable[[DataQuery], DataQuery],
    exception: type[Exception],
    message: str,
) -> None:
    """Test that appropriate Exceptions are raised."""
    query_config(query)
    with pytest.raises(exception, match=message):
        query.get_data()


@pytest.mark.parametrize(
    ("query_config", "request_xml"),
    [
        pytest.param(
            lambda q: (
                q.set_version_filter("Actuals")
                .set_time_filter("01/2026", "03/2026")
                .add_account_filter("Assets")
            ),
            ET.fromstring(
                '<call callerName="wdadaptivepy" method="exportData">'
                '  <credentials login="" password="" />'
                '  <format displayNameEnabled="true" includeCodes="true" includeDisplayNames="false" includeNames="true" includeUnmappedItems="false" useIds="false" useInternalCodes="true"/>'  # noqa: E501
                '  <version name="Actuals"/>'
                "  <filters>"
                "    <accounts>"
                '      <account code="Assets" includeDescendants="true" isAssumption="false"/>'  # noqa: E501
                "    </accounts>"
                '    <timeSpan end="03/2026" start="01/2026"/>'
                "  </filters>"
                '  <rules includeRollupAccounts="false" includeRollupLevels="false" includeZeroRows="false" markBlanks="false" markInvalidValues="false" timeRollups="false">'  # noqa: E501
                '    <currency useLocal="true"/>'
                "  </rules>"
                "</call>"
            ),
            id="test_minimal_request",
        ),
        pytest.param(
            lambda q: (
                q.set_version_filter(use_default=True)
                .set_time_filter("01/2026", "03/2026")
                .add_account_filter("Assets")
            ),
            ET.fromstring(
                '<call callerName="wdadaptivepy" method="exportData">'
                '  <credentials login="" password="" />'
                '  <format displayNameEnabled="true" includeCodes="true" includeDisplayNames="false" includeNames="true" includeUnmappedItems="false" useIds="false" useInternalCodes="true" />'  # noqa: E501
                '  <version isDefault="true" />'
                "  <filters>"
                "    <accounts>"
                '      <account code="Assets" includeDescendants="true" isAssumption="false" />'  # noqa: E501
                "    </accounts>"
                '    <timeSpan end="03/2026" start="01/2026" />'
                "  </filters>"
                '  <rules includeRollupAccounts="false" includeRollupLevels="false" includeZeroRows="false" markBlanks="false" markInvalidValues="false" timeRollups="false">'  # noqa: E501
                '    <currency useLocal="true" />'
                "  </rules>"
                "</call>"
            ),
            id="test_use_default_version",
        ),
        pytest.param(
            lambda q: (
                q.set_version_filter(Version(name="Actuals"))
                .set_time_filter("01/2026", "03/2026")
                .add_account_filter("Assets")
            ),
            ET.fromstring(
                '<call callerName="wdadaptivepy" method="exportData">'
                '  <credentials login="" password="" />'
                '  <format displayNameEnabled="true" includeCodes="true" includeDisplayNames="false" includeNames="true" includeUnmappedItems="false" useIds="false" useInternalCodes="true"/>'  # noqa: E501
                '  <version name="Actuals"/>'
                "  <filters>"
                "    <accounts>"
                '      <account code="Assets" includeDescendants="true" isAssumption="false"/>'  # noqa: E501
                "    </accounts>"
                '    <timeSpan end="03/2026" start="01/2026" />'
                "  </filters>"
                '  <rules includeRollupAccounts="false" includeRollupLevels="false" includeZeroRows="false" markBlanks="false" markInvalidValues="false" timeRollups="false">'  # noqa: E501
                '    <currency useLocal="true" />'
                "  </rules>"
                "</call>"
            ),
            id="test_version_model",
        ),
        pytest.param(
            lambda q: (
                q.set_version_filter("Actuals")
                .set_time_filter("01/2026", "03/2026", stratum="Year")
                .add_account_filter("Assets")
            ),
            ET.fromstring(
                '<call callerName="wdadaptivepy" method="exportData">'
                '  <credentials login="" password="" />'
                '  <format displayNameEnabled="true" includeCodes="true" includeDisplayNames="false" includeNames="true" includeUnmappedItems="false" useIds="false" useInternalCodes="true" />'  # noqa: E501
                '  <version name="Actuals" />'
                "  <filters>"
                "    <accounts>"
                '      <account code="Assets" includeDescendants="true" isAssumption="false" />'  # noqa: E501
                "    </accounts>"
                '    <timeSpan end="03/2026" start="01/2026" stratum="Year" />'
                "  </filters>"
                '  <rules includeRollupAccounts="false" includeRollupLevels="false" includeZeroRows="false" markBlanks="false" markInvalidValues="false" timeRollups="false">'  # noqa: E501
                '    <currency useLocal="true" />'
                "  </rules>"
                "</call>"
            ),
            id="test_stratum",
        ),
        pytest.param(
            lambda q: (
                q.set_version_filter("Actuals")
                .set_time_filter(
                    Period(code="01/2026"),
                    Period(code="03/2026"),
                    stratum=Stratum(code="Year"),
                )
                .add_account_filter("Assets")
            ),
            ET.fromstring(
                '<call callerName="wdadaptivepy" method="exportData">'
                '  <credentials login="" password="" />'
                '  <format displayNameEnabled="true" includeCodes="true" includeDisplayNames="false" includeNames="true" includeUnmappedItems="false" useIds="false" useInternalCodes="true" />'  # noqa: E501
                '  <version name="Actuals" />'
                "  <filters>"
                "    <accounts>"
                '      <account code="Assets" includeDescendants="true" isAssumption="false" />'  # noqa: E501
                "    </accounts>"
                '    <timeSpan end="03/2026" start="01/2026" stratum="Year" />'
                "  </filters>"
                '  <rules includeRollupAccounts="false" includeRollupLevels="false" includeZeroRows="false" markBlanks="false" markInvalidValues="false" timeRollups="false">'  # noqa: E501
                '    <currency useLocal="true" />'
                "  </rules>"
                "</call>"
            ),
            id="test_stratum_models",
        ),
        pytest.param(
            lambda q: (
                q.set_version_filter("Actuals")
                .set_time_filter("01/2026", "03/2026")
                .add_account_filter(Account(code="Assets", is_assumption=False))
            ),
            ET.fromstring(
                '<call callerName="wdadaptivepy" method="exportData">'
                '  <credentials login="" password="" />'
                '  <format displayNameEnabled="true" includeCodes="true" includeDisplayNames="false" includeNames="true" includeUnmappedItems="false" useIds="false" useInternalCodes="true" />'  # noqa: E501
                '  <version name="Actuals" />'
                "  <filters>"
                "    <accounts>"
                '      <account code="Assets" includeDescendants="true" isAssumption="false" />'  # noqa: E501
                "    </accounts>"
                '    <timeSpan end="03/2026" start="01/2026" />'
                "  </filters>"
                '  <rules includeRollupAccounts="false" includeRollupLevels="false" includeZeroRows="false" markBlanks="false" markInvalidValues="false" timeRollups="false">'  # noqa: E501
                '    <currency useLocal="true" />'
                "  </rules>"
                "</call>"
            ),
            id="test_account_model_not_assumption",
        ),
        pytest.param(
            lambda q: (
                q.set_version_filter("Actuals")
                .set_time_filter("01/2026", "03/2026")
                .add_account_filter(Account(code="Assets", is_assumption=True))
            ),
            ET.fromstring(
                '<call callerName="wdadaptivepy" method="exportData">'
                '  <credentials login="" password="" />'
                '  <format displayNameEnabled="true" includeCodes="true" includeDisplayNames="false" includeNames="true" includeUnmappedItems="false" useIds="false" useInternalCodes="true" />'  # noqa: E501
                '  <version name="Actuals" />'
                "  <filters>"
                "    <accounts>"
                '      <account code="Assets" includeDescendants="true" isAssumption="true" />'  # noqa: E501
                "    </accounts>"
                '    <timeSpan end="03/2026" start="01/2026" />'
                "  </filters>"
                '  <rules includeRollupAccounts="false" includeRollupLevels="false" includeZeroRows="false" markBlanks="false" markInvalidValues="false" timeRollups="false">'  # noqa: E501
                '    <currency useLocal="true" />'
                "  </rules>"
                "</call>"
            ),
            id="test_account_model_is_assumption",
        ),
        pytest.param(
            lambda q: (
                q.set_version_filter("Actuals")
                .set_time_filter("01/2026", "03/2026")
                .add_account_filter("Assets", include_descendants=True)
            ),
            ET.fromstring(
                '<call callerName="wdadaptivepy" method="exportData">'
                '  <credentials login="" password="" />'
                '  <format displayNameEnabled="true" includeCodes="true" includeDisplayNames="false" includeNames="true" includeUnmappedItems="false" useIds="false" useInternalCodes="true" />'  # noqa: E501
                '  <version name="Actuals" />'
                "  <filters>"
                "    <accounts>"
                '      <account code="Assets" includeDescendants="true" isAssumption="false" />'  # noqa: E501
                "    </accounts>"
                '    <timeSpan end="03/2026" start="01/2026" />'
                "  </filters>"
                '  <rules includeRollupAccounts="false" includeRollupLevels="false" includeZeroRows="false" markBlanks="false" markInvalidValues="false" timeRollups="false">'  # noqa: E501
                '    <currency useLocal="true" />'
                "  </rules>"
                "</call>"
            ),
            id="test_account_include_descendants",
        ),
        pytest.param(
            lambda q: (
                q.set_version_filter("Actuals")
                .set_time_filter("01/2026", "03/2026")
                .add_account_filter("Assets", include_descendants=False)
            ),
            ET.fromstring(
                '<call callerName="wdadaptivepy" method="exportData">'
                '  <credentials login="" password="" />'
                '  <format displayNameEnabled="true" includeCodes="true" includeDisplayNames="false" includeNames="true" includeUnmappedItems="false" useIds="false" useInternalCodes="true" />'  # noqa: E501
                '  <version name="Actuals" />'
                "  <filters>"
                "    <accounts>"
                '      <account code="Assets" includeDescendants="false" isAssumption="false" />'  # noqa: E501
                "    </accounts>"
                '    <timeSpan end="03/2026" start="01/2026" />'
                "  </filters>"
                '  <rules includeRollupAccounts="false" includeRollupLevels="false" includeZeroRows="false" markBlanks="false" markInvalidValues="false" timeRollups="false">'  # noqa: E501
                '    <currency useLocal="true" />'
                "  </rules>"
                "</call>"
            ),
            id="test_account_exclude_descendants",
        ),
        pytest.param(
            lambda q: (
                q.set_version_filter("Actuals")
                .set_time_filter("01/2026", "03/2026")
                .add_account_filter(["Assets", "Liabilities"])
            ),
            ET.fromstring(
                '<call callerName="wdadaptivepy" method="exportData">'
                '  <credentials login="" password="" />'
                '  <format displayNameEnabled="true" includeCodes="true" includeDisplayNames="false" includeNames="true" includeUnmappedItems="false" useIds="false" useInternalCodes="true" />'  # noqa: E501
                '  <version name="Actuals" />'
                "  <filters>"
                "    <accounts>"
                '      <account code="Assets" includeDescendants="true" isAssumption="false" />'  # noqa: E501
                '      <account code="Liabilities" includeDescendants="true" isAssumption="false" />'  # noqa: E501
                "    </accounts>"
                '    <timeSpan end="03/2026" start="01/2026" />'
                "  </filters>"
                '  <rules includeRollupAccounts="false" includeRollupLevels="false" includeZeroRows="false" markBlanks="false" markInvalidValues="false" timeRollups="false">'  # noqa: E501
                '    <currency useLocal="true" />'
                "  </rules>"
                "</call>"
            ),
            id="test_list_accounts",
        ),
        pytest.param(
            lambda q: (
                q.set_version_filter("Actuals")
                .set_time_filter("01/2026", "03/2026")
                .add_account_filter(
                    [
                        Account(code="Assets", is_assumption=False),
                        Account(code="Liabilities", is_assumption=True),
                    ]
                )
            ),
            ET.fromstring(
                '<call callerName="wdadaptivepy" method="exportData">'
                '  <credentials login="" password="" />'
                '  <format displayNameEnabled="true" includeCodes="true" includeDisplayNames="false" includeNames="true" includeUnmappedItems="false" useIds="false" useInternalCodes="true" />'  # noqa: E501
                '  <version name="Actuals" />'
                "  <filters>"
                "    <accounts>"
                '      <account code="Assets" includeDescendants="true" isAssumption="false" />'  # noqa: E501
                '      <account code="Liabilities" includeDescendants="true" isAssumption="true" />'  # noqa: E501
                "    </accounts>"
                '    <timeSpan end="03/2026" start="01/2026" />'
                "  </filters>"
                '  <rules includeRollupAccounts="false" includeRollupLevels="false" includeZeroRows="false" markBlanks="false" markInvalidValues="false" timeRollups="false">'  # noqa: E501
                '    <currency useLocal="true" />'
                "  </rules>"
                "</call>"
            ),
            id="test_list_accounts_models",
        ),
        pytest.param(
            lambda q: (
                q.set_version_filter("Actuals")
                .set_time_filter("01/2026", "03/2026")
                .add_account_filter("Assets")
                .add_account_filter("Liabilities")
            ),
            ET.fromstring(
                '<call callerName="wdadaptivepy" method="exportData">'
                '  <credentials login="" password="" />'
                '  <format displayNameEnabled="true" includeCodes="true" includeDisplayNames="false" includeNames="true" includeUnmappedItems="false" useIds="false" useInternalCodes="true" />'  # noqa: E501
                '  <version name="Actuals" />'
                "  <filters>"
                "    <accounts>"
                '      <account code="Assets" includeDescendants="true" isAssumption="false" />'  # noqa: E501
                '      <account code="Liabilities" includeDescendants="true" isAssumption="false" />'  # noqa: E501
                "    </accounts>"
                '    <timeSpan end="03/2026" start="01/2026" />'
                "  </filters>"
                '  <rules includeRollupAccounts="false" includeRollupLevels="false" includeZeroRows="false" markBlanks="false" markInvalidValues="false" timeRollups="false">'  # noqa: E501
                '    <currency useLocal="true" />'
                "  </rules>"
                "</call>"
            ),
            id="test_multiple_accounts",
        ),
        pytest.param(
            lambda q: (
                q.set_version_filter("Actuals")
                .set_time_filter("01/2026", "03/2026")
                .add_account_filter(Account(code="Assets", is_assumption=False))
                .add_account_filter(Account(code="Liabilities", is_assumption=True))
            ),
            ET.fromstring(
                '<call callerName="wdadaptivepy" method="exportData">'
                '  <credentials login="" password="" />'
                '  <format displayNameEnabled="true" includeCodes="true" includeDisplayNames="false" includeNames="true" includeUnmappedItems="false" useIds="false" useInternalCodes="true" />'  # noqa: E501
                '  <version name="Actuals" />'
                "  <filters>"
                "    <accounts>"
                '      <account code="Assets" includeDescendants="true" isAssumption="false" />'  # noqa: E501
                '      <account code="Liabilities" includeDescendants="true" isAssumption="true" />'  # noqa: E501
                "    </accounts>"
                '    <timeSpan end="03/2026" start="01/2026" />'
                "  </filters>"
                '  <rules includeRollupAccounts="false" includeRollupLevels="false" includeZeroRows="false" markBlanks="false" markInvalidValues="false" timeRollups="false">'  # noqa: E501
                '    <currency useLocal="true" />'
                "  </rules>"
                "</call>"
            ),
            id="test_multiple_accounts_models",
        ),
        pytest.param(
            lambda q: (
                q.set_version_filter("Actuals")
                .set_time_filter("01/2026", "03/2026")
                .add_account_filter("Assets")
                .add_dimension_value_filter("Vendor", "Test")
            ),
            ET.fromstring(
                '<call callerName="wdadaptivepy" method="exportData">'
                '  <credentials login="" password="" />'
                '  <format displayNameEnabled="true" includeCodes="true" includeDisplayNames="false" includeNames="true" includeUnmappedItems="false" useIds="false" useInternalCodes="true" />'  # noqa: E501
                '  <version name="Actuals" />'
                "  <filters>"
                "    <accounts>"
                '      <account code="Assets" includeDescendants="true" isAssumption="false" />'  # noqa: E501
                "    </accounts>"
                "    <dimensionValues>"
                '      <dimensionValue dimName="Vendor" code="Test" />'
                "    </dimensionValues>"
                '    <timeSpan end="03/2026" start="01/2026" />'
                "  </filters>"
                "  <dimensions>"
                '    <dimension name="Vendor" />'
                "  </dimensions>"
                '  <rules includeRollupAccounts="false" includeRollupLevels="false" includeZeroRows="false" markBlanks="false" markInvalidValues="false" timeRollups="false">'  # noqa: E501
                '    <currency useLocal="true" />'
                "  </rules>"
                "</call>"
            ),
            id="test_dimension_value_filter",
        ),
        pytest.param(
            lambda q: (
                q.set_version_filter("Actuals")
                .set_time_filter("01/2026", "03/2026")
                .add_account_filter("Assets")
                .add_dimension_value_filter("Vendor", ["Test", "Another"])
            ),
            ET.fromstring(
                '<call callerName="wdadaptivepy" method="exportData">'
                '  <credentials login="" password="" />'
                '  <format displayNameEnabled="true" includeCodes="true" includeDisplayNames="false" includeNames="true" includeUnmappedItems="false" useIds="false" useInternalCodes="true" />'  # noqa: E501
                '  <version name="Actuals" />'
                "  <filters>"
                "    <accounts>"
                '      <account code="Assets" includeDescendants="true" isAssumption="false" />'  # noqa: E501
                "    </accounts>"
                "    <dimensionValues>"
                '      <dimensionValue dimName="Vendor" code="Test" />'
                '      <dimensionValue dimName="Vendor" code="Another" />'
                "    </dimensionValues>"
                '    <timeSpan end="03/2026" start="01/2026" />'
                "  </filters>"
                "  <dimensions>"
                '    <dimension name="Vendor" />'
                "  </dimensions>"
                '  <rules includeRollupAccounts="false" includeRollupLevels="false" includeZeroRows="false" markBlanks="false" markInvalidValues="false" timeRollups="false">'  # noqa: E501
                '    <currency useLocal="true" />'
                "  </rules>"
                "</call>"
            ),
            id="test_dimension_value_filter_list",
        ),
        pytest.param(
            lambda q: (
                q.set_version_filter("Actuals")
                .set_time_filter("01/2026", "03/2026")
                .add_account_filter("Assets")
                .add_dimension_value_filter("Vendor", "Test")
                .add_dimension_value_filter("Vendor", "Another")
            ),
            ET.fromstring(
                '<call callerName="wdadaptivepy" method="exportData">'
                '  <credentials login="" password="" />'
                '  <format displayNameEnabled="true" includeCodes="true" includeDisplayNames="false" includeNames="true" includeUnmappedItems="false" useIds="false" useInternalCodes="true" />'  # noqa: E501
                '  <version name="Actuals" />'
                "  <filters>"
                "    <accounts>"
                '      <account code="Assets" includeDescendants="true" isAssumption="false" />'  # noqa: E501
                "    </accounts>"
                "    <dimensionValues>"
                '      <dimensionValue dimName="Vendor" code="Test" />'
                '      <dimensionValue dimName="Vendor" code="Another" />'
                "    </dimensionValues>"
                '    <timeSpan end="03/2026" start="01/2026" />'
                "  </filters>"
                "  <dimensions>"
                '    <dimension name="Vendor" />'
                "  </dimensions>"
                '  <rules includeRollupAccounts="false" includeRollupLevels="false" includeZeroRows="false" markBlanks="false" markInvalidValues="false" timeRollups="false">'  # noqa: E501
                '    <currency useLocal="true" />'
                "  </rules>"
                "</call>"
            ),
            id="test_dimension_value_filter_multiple",
        ),
        pytest.param(
            lambda q: (
                q.set_version_filter("Actuals")
                .set_time_filter("01/2026", "03/2026")
                .add_account_filter("Assets")
                .add_dimension_value_filter("Vendor", ["Test1", "Test2"])
                .add_dimension_value_filter("Vendor", ["Another1", "Another2"])
            ),
            ET.fromstring(
                '<call callerName="wdadaptivepy" method="exportData">'
                '  <credentials login="" password="" />'
                '  <format displayNameEnabled="true" includeCodes="true" includeDisplayNames="false" includeNames="true" includeUnmappedItems="false" useIds="false" useInternalCodes="true" />'  # noqa: E501
                '  <version name="Actuals" />'
                "  <filters>"
                "    <accounts>"
                '      <account code="Assets" includeDescendants="true" isAssumption="false" />'  # noqa: E501
                "    </accounts>"
                "    <dimensionValues>"
                '      <dimensionValue dimName="Vendor" code="Test1" />'
                '      <dimensionValue dimName="Vendor" code="Test2" />'
                '      <dimensionValue dimName="Vendor" code="Another1" />'
                '      <dimensionValue dimName="Vendor" code="Another2" />'
                "    </dimensionValues>"
                '    <timeSpan end="03/2026" start="01/2026" />'
                "  </filters>"
                "  <dimensions>"
                '    <dimension name="Vendor" />'
                "  </dimensions>"
                '  <rules includeRollupAccounts="false" includeRollupLevels="false" includeZeroRows="false" markBlanks="false" markInvalidValues="false" timeRollups="false">'  # noqa: E501
                '    <currency useLocal="true" />'
                "  </rules>"
                "</call>"
            ),
            id="test_dimension_value_filter_multiple",
        ),
        pytest.param(
            lambda q: (
                q.set_version_filter("Actuals")
                .set_time_filter("01/2026", "03/2026")
                .add_account_filter("Assets")
                .add_dimension_value_filter("Vendor", ["Test1", "Test2"])
                .add_dimension_value_filter("Customer", ["Another1", "Another2"])
            ),
            ET.fromstring(
                '<call callerName="wdadaptivepy" method="exportData">'
                '  <credentials login="" password="" />'
                '  <format displayNameEnabled="true" includeCodes="true" includeDisplayNames="false" includeNames="true" includeUnmappedItems="false" useIds="false" useInternalCodes="true" />'  # noqa: E501
                '  <version name="Actuals" />'
                "  <filters>"
                "    <accounts>"
                '      <account code="Assets" includeDescendants="true" isAssumption="false" />'  # noqa: E501
                "    </accounts>"
                "    <dimensionValues>"
                '      <dimensionValue dimName="Vendor" code="Test1" />'
                '      <dimensionValue dimName="Vendor" code="Test2" />'
                '      <dimensionValue dimName="Customer" code="Another1" />'
                '      <dimensionValue dimName="Customer" code="Another2" />'
                "    </dimensionValues>"
                '    <timeSpan end="03/2026" start="01/2026" />'
                "  </filters>"
                "  <dimensions>"
                '    <dimension name="Vendor" />'
                '    <dimension name="Customer" />'
                "  </dimensions>"
                '  <rules includeRollupAccounts="false" includeRollupLevels="false" includeZeroRows="false" markBlanks="false" markInvalidValues="false" timeRollups="false">'  # noqa: E501
                '    <currency useLocal="true" />'
                "  </rules>"
                "</call>"
            ),
            id="test_dimension_value_filter_multiple_different_dimension",
        ),
        pytest.param(
            lambda q: (
                q.set_version_filter("Actuals")
                .set_time_filter("01/2026", "03/2026")
                .add_account_filter("Assets")
                .add_dimension_value_filter(
                    "Vendor", ["Test1", "Test2"], direct_children=True
                )
                .add_dimension_value_filter(
                    "Customer", ["Another1", "Another2"], direct_children=False
                )
            ),
            ET.fromstring(
                '<call callerName="wdadaptivepy" method="exportData">'
                '  <credentials login="" password="" />'
                '  <format displayNameEnabled="true" includeCodes="true" includeDisplayNames="false" includeNames="true" includeUnmappedItems="false" useIds="false" useInternalCodes="true" />'  # noqa: E501
                '  <version name="Actuals" />'
                "  <filters>"
                "    <accounts>"
                '      <account code="Assets" includeDescendants="true" isAssumption="false" />'  # noqa: E501
                "    </accounts>"
                "    <dimensionValues>"
                '      <dimensionValue dimName="Vendor" code="Test1" directChildren="true" />'  # noqa: E501
                '      <dimensionValue dimName="Vendor" code="Test2" directChildren="true" />'  # noqa: E501
                '      <dimensionValue dimName="Customer" code="Another1" directChildren="false" />'  # noqa: E501
                '      <dimensionValue dimName="Customer" code="Another2" directChildren="false" />'  # noqa: E501
                "    </dimensionValues>"
                '    <timeSpan end="03/2026" start="01/2026" />'
                "  </filters>"
                "  <dimensions>"
                '    <dimension name="Vendor" />'
                '    <dimension name="Customer" />'
                "  </dimensions>"
                '  <rules includeRollupAccounts="false" includeRollupLevels="false" includeZeroRows="false" markBlanks="false" markInvalidValues="false" timeRollups="false">'  # noqa: E501
                '    <currency useLocal="true" />'
                "  </rules>"
                "</call>"
            ),
            id="test_dimension_value_filter_multiple_different_dimension",
        ),
    ],
)
def test_data_query_request_xml(
    query: DataQuery,
    query_config: Callable[[DataQuery], DataQuery],
    request_xml: ET.Element,
) -> None:
    """Test that appropriate XML request bodies are generated."""
    query_config(query)
    actual_xml = query._DataQuery__xml_api._XMLApi__generate_xml_call(  # noqa: SLF001  # pyright: ignore[reportAttributeAccessIssue]
        "exportData",
        query._generate_xml(),  # noqa: SLF001
    )
    ET.indent(actual_xml)
    ET.indent(request_xml)
    assert ET.canonicalize(ET.tostring(actual_xml).decode()) == ET.canonicalize(
        ET.tostring(request_xml).decode()
    )
