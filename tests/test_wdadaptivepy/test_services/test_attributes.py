"""Tests for wdadaptivepy's service for Adaptive's Attributes."""

# Code using pytest-mock
from unittest.mock import MagicMock
from xml.etree import ElementTree as ET

import pytest
from pytest_mock import MockerFixture

from wdadaptivepy.connectors.xml_api.xml_api import XMLApi
from wdadaptivepy.models import Attribute, AttributeValue, MetadataList
from wdadaptivepy.services import AttributeService

tests: list[tuple[ET.Element, MetadataList[Attribute]]] = []
test_with_errors: list[tuple[ET.Element, MetadataList[Attribute], int, str]] = []


# Attributes for all tests
av118 = AttributeValue(id=118, name="No")
av117 = AttributeValue(id=117, name="Yes")
av136 = AttributeValue(id=136, name="Full")
av135 = AttributeValue(id=135, name="Partial")

av136.set_adaptive_parent(av117)
av135.set_adaptive_parent(av117)

a13 = Attribute(
    id=13,
    name="AP Eligible",
    attribute_type="account",
)

# TEST 2 # Empty xml returns empty MetadataList
xml2 = ET.fromstring("""<?xml version='1.0' encoding='UTF-8'?>
<response success='true'>
  <output>
  </output>
</response>""")
tests.append((xml2, MetadataList([])))

# TEST 2 # TODO: Include whole example from docs  # noqa: FIX002, TD002, TD003
xml4 = ET.fromstring("""<?xml version='1.0' encoding='UTF-8'?>
<response success='true'>
  <output>
    <attributes>
      <attribute id="13" name="AP Eligible" type="account" seqNo="21">
         <attributeValue id="118" name="No" />
         <attributeValue id="117" name="Yes">
           <attributeValue id="136" name="Full" />
           <attributeValue id="135" name="Partial" />
         </attributeValue>
       </attribute>
    </attributes>
  </output>
</response>
""")

tests.append(
    (
        xml4,
        MetadataList(
            [a13],
        ),
    ),
)


# From here down, we're using the original testing methodology
@pytest.fixture
def account_service() -> AttributeService:
    """Fixture for wdadaptivepy's Attribute Service.

    Returns:
        wdadaptivepy AttributeService

    """
    xml_api_instance = XMLApi("", "")
    return AttributeService(xml_api=xml_api_instance)


@pytest.fixture
def mock_attributes(
    mocker: MockerFixture,
    account_service: AttributeService,
) -> ET.Element:
    """Mock Adaptive's response from exportAttribute XML API.

    Args:
        mocker: pytest's mocker
        account_service: wdadaptivepy AttributeService to mock

    Returns:
        XML Element

    """
    # Create a mock object for the Attributes
    mocked_levels = mocker.MagicMock()
    mocker.patch.object(
        account_service._AttributeService__xml_api,  # noqa: SLF001  # pyright: ignore[reportAttributeAccessIssue]
        "make_xml_request",
        mocked_levels,
    )
    return mocked_levels


@pytest.mark.parametrize(("element", "expected"), tests)
def test_get_all(
    element: ET.Element,
    expected: MetadataList[Attribute],
    account_service: AttributeService,
    mock_attributes: MagicMock,
) -> None:
    """Tests that wdadaptivepy properly parses Adaptive's exportAttributes API response.

    Args:
        element: Adaptive's exportAttributes XML API response
        expected: wdadaptivepy MetadataList of Attributes
        account_service: wdadaptivepy AttributeService
        mock_attributes: Mocker for Adaptive's exportAttributes XML API response

    """
    # Set the mock object to return a specific response
    mock_attributes.return_value = element

    # Call the function that downloads data from the external service
    levels = account_service.get_all()

    # Verify that the function returns the expected data
    assert levels == expected


@pytest.mark.parametrize(
    ("element", "expected", "index_with_error", "key_with_error"),
    test_with_errors,
)
def test_get_all_with_errors(  # noqa: PLR0913
    element: ET.Element,
    expected: MetadataList[Attribute],
    index_with_error: int,
    key_with_error: str,
    attribute_service: AttributeService,
    mock_levels: MagicMock,
) -> None:
    """Tests that wdadaptivepy properly parses Adaptive's exportAttributes API response.

    Args:
        element: Adaptive's exportAttributes XML API response
        expected: wdadaptivepy MetadataList of Attributes
        index_with_error: the item in the MetadataList that shouldn't match
        key_with_error: the key for the property in that item that should't match
        attribute_service: wdadaptivepy AttributeService
        mock_levels: Mocker for Adaptive's exportAttributes XML API response

    """
    # Set the mock object to return a specific response
    mock_levels.return_value = element

    # Call the function that downloads data from the external service
    levels = attribute_service.get_all()

    # Verify that the function returns the expected data
    xml_value = getattr(levels[index_with_error], key_with_error, None)
    expected_value = getattr(expected[index_with_error], key_with_error, None)
    assert xml_value != expected_value
