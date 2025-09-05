"""Tests for wdadaptivepy's service for Adaptive's PermissionSets."""

# Code using pytest-mock
from unittest.mock import MagicMock
from xml.etree import ElementTree as ET

import pytest
from pytest_mock import MockerFixture

from wdadaptivepy.connectors.xml_api.xml_api import XMLApi
from wdadaptivepy.models import (
    MetadataList,
    PermissionSet,
)
from wdadaptivepy.services import PermissionSetService

tests: list[tuple[ET.Element, MetadataList[PermissionSet]]] = []
test_with_errors: list[tuple[ET.Element, MetadataList[PermissionSet], int, str]] = []

# Create PermissionSets for tests
ps1 = PermissionSet(id=1, name="Standard", permissions="SHT,RPT,SCOREBOARD")
ps2 = PermissionSet(
    id=2,
    name="Administrative",
    permissions="SHT,RPT,SCOREBOARD,SAL,MOD,IMP,EXP",
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
   <permission_sets>
     <permission_set id="1" name="Standard" permissions="SHT,RPT,SCOREBOARD"/>
     <permission_set id="2" name="Administrative" permissions="SHT,RPT,SCOREBOARD,SAL,MOD,IMP,EXP"/>
   </permission_sets>
 </output>
</response>""")  # noqa: E501

tests.append(
    (
        xml2,
        MetadataList([ps1, ps2]),
    ),
)


# From here down, we're using the original testing methodology
@pytest.fixture
def permission_set_service() -> PermissionSetService:
    """Fixture for wdadaptivepy's PermissionSet Service.

    Returns:
        wdadaptivepy PermissionSetService

    """
    xml_api_instance = XMLApi("", "")
    return PermissionSetService(xml_api=xml_api_instance)


@pytest.fixture
def mock_permission_sets(
    mocker: MockerFixture,
    permission_set_service: PermissionSetService,
) -> ET.Element:
    """Mock Adaptive's response from exportPermissionSets XML API.

    Args:
        mocker: pytest's mocker
        permission_set_service: wdadaptivepy PermissionSetService to mock

    Returns:
        XML Element

    """
    # Create a mock object for the PermissionSets
    mocked_levels = mocker.MagicMock()
    mocker.patch.object(
        permission_set_service._PermissionSetService__xml_api,  # noqa: SLF001  # pyright: ignore[reportAttributeAccessIssue]
        "make_xml_request",
        mocked_levels,
    )
    return mocked_levels


@pytest.mark.parametrize(("element", "expected"), tests)
def test_get_all(
    element: ET.Element,
    expected: MetadataList[PermissionSet],
    permission_set_service: PermissionSetService,
    mock_permission_sets: MagicMock,
) -> None:
    """Tests that wdadaptivepy properly parses the exportPermissionSets API response.

    Args:
        element: Adaptive's exportPermissionSets XML API response
        expected: wdadaptivepy MetadataList of PermissionSets
        permission_set_service: wdadaptivepy PermissionSetService
        mock_permission_sets: Mocker for Adaptive's exportPermissionSets API response

    """
    # Set the mock object to return a specific response
    mock_permission_sets.return_value = element

    # Call the function that downloads data from the external service
    levels = permission_set_service.get_all()

    # Verify that the function returns the expected data
    assert levels == expected


@pytest.mark.parametrize(
    ("element", "expected", "index_with_error", "key_with_error"),
    test_with_errors,
)
def test_get_all_with_errors(  # noqa: PLR0913
    element: ET.Element,
    expected: MetadataList[PermissionSet],
    index_with_error: int,
    key_with_error: str,
    permission_set_service: PermissionSetService,
    mock_permission_sets: MagicMock,
) -> None:
    """Tests that wdadaptivepy properly parses the exportPermissionSets API response.

    Args:
        element: Adaptive's exportPermissionSets XML API response
        expected: wdadaptivepy MetadataList of PermissionSets
        index_with_error: the item in the MetadataList that shouldn't match
        key_with_error: the key for the property in that item that should't match
        permission_set_service: wdadaptivepy PermissionSetService
        mock_permission_sets: Mocker for Adaptive's exportPermissionSets API response

    """
    # Set the mock object to return a specific response
    mock_permission_sets.return_value = element

    # Call the function that downloads data from the external service
    levels = permission_set_service.get_all()

    # Verify that the function returns the expected data
    xml_value = getattr(levels[index_with_error], key_with_error, None)
    expected_value = getattr(expected[index_with_error], key_with_error, None)
    assert xml_value != expected_value
