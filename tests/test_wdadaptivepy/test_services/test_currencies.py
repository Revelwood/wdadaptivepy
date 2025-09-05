"""Tests for wdadaptivepy's service for Adaptive's Currencies."""

# Code using pytest-mock
from unittest.mock import MagicMock
from xml.etree import ElementTree as ET

import pytest
from pytest_mock import MockerFixture

from wdadaptivepy.connectors.xml_api.xml_api import XMLApi
from wdadaptivepy.models import Currency, MetadataList
from wdadaptivepy.services import CurrencyService

tests: list[tuple[ET.Element, MetadataList[Currency]]] = []
test_with_errors: list[tuple[ET.Element, MetadataList[Currency], int, str]] = []

# Create Currencies
c2 = Currency(
    id=2,
    code="EUR",
    precision="4",
    is_reporting_currency=False,
    user_defined=False,
    description="Euro Member Countries, Euro",
)

c3 = Currency(
    id=3,
    code="EUR1",
    precision="4",
    is_reporting_currency=False,
    user_defined=True,
    description="User-defined Euro 1",
)

c1 = Currency(
    id=1,
    code="USD",
    precision="2",
    is_reporting_currency=True,
    user_defined=False,
    description="United States of America, Dollars",
)

# TEST 1 ######################################################################
xml1 = ET.fromstring("""<?xml version='1.0' encoding='UTF-8'?>
<response success='true'>
  <output>
  </output>
</response>""")
tests.append((xml1, MetadataList([])))

# TEST 2 ######################################################################
xml2 = ET.fromstring("""<?xml version='1.0' encoding='UTF-8'?>
<response success="true">
<output>
<currencies seqNo="42">
  <currency id="2" code="EUR"  precision="4" isReportingCurrency="0" userDefined="0" description="Euro Member Countries, Euro" />
  <currency id="3" code="EUR1" precision="4" isReportingCurrency="0" userDefined="1" description="User-defined Euro 1" />
  <currency id="1" code="USD" precision="2" isReportingCurrency="1" userDefined="0" description="United States of America, Dollars" />
</currencies>
</output>
</response>""")  # noqa: E501

tests.append(
    (
        xml2,
        MetadataList([c2, c3, c1]),
    ),
)


# From here down, we're using the original testing methodology
@pytest.fixture
def currency_service() -> CurrencyService:
    """Fixture for wdadaptivepy's Currency Service.

    Returns:
        wdadaptivepy CurrencyService

    """
    xml_api_instance = XMLApi("", "")
    return CurrencyService(xml_api=xml_api_instance)


@pytest.fixture
def mock_currencies(
    mocker: MockerFixture,
    currency_service: CurrencyService,
) -> ET.Element:
    """Mock Adaptive's response from exportCurrencies XML API.

    Args:
        mocker: pytest's mocker
        currency_service: wdadaptivepy CurrencyService to mock

    Returns:
        XML Element

    """
    # Create a mock object for the Currencies
    mocked_levels = mocker.MagicMock()
    mocker.patch.object(
        currency_service._CurrencyService__xml_api,  # noqa: SLF001  # pyright: ignore[reportAttributeAccessIssue]
        "make_xml_request",
        mocked_levels,
    )
    return mocked_levels


@pytest.mark.parametrize(("element", "expected"), tests)
def test_get_all(
    element: ET.Element,
    expected: MetadataList[Currency],
    currency_service: CurrencyService,
    mock_currencies: MagicMock,
) -> None:
    """Tests that wdadaptivepy properly parses Adaptive's exportCurrencies API response.

    Args:
        element: Adaptive's exportCurrencies XML API response
        expected: wdadaptivepy MetadataList of Currencies
        currency_service: wdadaptivepy CurrencyService
        mock_currencies: Mocker for Adaptive's exportCurrencies XML API response

    """
    # Set the mock object to return a specific response
    mock_currencies.return_value = element

    # Call the function that downloads data from the external service
    levels = currency_service.get_all()

    # Verify that the function returns the expected data
    assert levels == expected


@pytest.mark.parametrize(
    ("element", "expected", "index_with_error", "key_with_error"),
    test_with_errors,
)
def test_get_all_with_errors(  # noqa: PLR0913
    element: ET.Element,
    expected: MetadataList[Currency],
    index_with_error: int,
    key_with_error: str,
    currency_service: CurrencyService,
    mock_currencies: MagicMock,
) -> None:
    """Tests that wdadaptivepy properly parses Adaptive's exportCurrencies API response.

    Args:
        element: Adaptive's exportCurrencies XML API response
        expected: wdadaptivepy MetadataList of Currencies
        index_with_error: the item in the MetadataList that shouldn't match
        key_with_error: the key for the property in that item that should't match
        currency_service: wdadaptivepy CurrencyService
        mock_currencies: Mocker for Adaptive's exportCurrencies XML API response

    """
    # Set the mock object to return a specific response
    mock_currencies.return_value = element

    # Call the function that downloads data from the external service
    levels = currency_service.get_all()

    # Verify that the function returns the expected data
    xml_value = getattr(levels[index_with_error], key_with_error, None)
    expected_value = getattr(expected[index_with_error], key_with_error, None)
    assert xml_value != expected_value
