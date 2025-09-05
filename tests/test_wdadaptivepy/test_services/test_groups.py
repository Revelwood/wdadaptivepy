"""Tests for wdadaptivepy's service for Adaptive's Groups."""

# Code using pytest-mock
from unittest.mock import MagicMock
from xml.etree import ElementTree as ET

import pytest
from pytest_mock import MockerFixture

from wdadaptivepy.connectors.xml_api.xml_api import XMLApi
from wdadaptivepy.models import (
    Group,
    MetadataList,
)
from wdadaptivepy.services import GroupService

tests: list[tuple[ET.Element, MetadataList[Group]]] = []
test_with_errors: list[tuple[ET.Element, MetadataList[Group], int, str]] = []

# Create Groups
g1 = Group(id=1, name="Corporate and Operations", is_global=True)
g2 = Group(id=2, name="Admins", is_global=True)
g3 = Group(id=3, name="Ops and Admins", is_global=True)
g4 = Group(id=4, name="My group", is_global=False, owner_id="3")


# TEST 1 ######################################################################
xml1 = ET.fromstring("""<?xml version='1.0' encoding='UTF-8'?>
<response success='true'>
  <output>
  </output>
</response>""")
tests.append((xml1, MetadataList([])))

# TEST 2 ######################################################################
xml2 = ET.fromstring("""<?xml version="1.0" encoding="UTF-8"?>
<response success="true">
 <output>
    <groups>
       <group id="1" name="Corporate and Operations" isGlobal="true"/>
       <group id="2" name="Admins" isGlobal="true"/>
       <group id="3" name="Ops and Admins" isGlobal="true"/>
       <group id="4" name="My group" isGlobal="false" ownerId="3"/>
    </groups>
 </output>
</response>""")

tests.append(
    (
        xml2,
        MetadataList([g1, g2, g3, g4]),
    ),
)


# From here down, we're using the original testing methodology
@pytest.fixture
def group_service() -> GroupService:
    """Fixture for wdadaptivepy's Group Service.

    Returns:
        wdadaptivepy GroupService

    """
    xml_api_instance = XMLApi("", "")
    return GroupService(xml_api=xml_api_instance)


@pytest.fixture
def mock_groups(
    mocker: MockerFixture,
    group_service: GroupService,
) -> ET.Element:
    """Mock Adaptive's response from exportGroups XML API.

    Args:
        mocker: pytest's mocker
        group_service: wdadaptivepy GroupService to mock

    Returns:
        XML Element

    """
    # Create a mock object for the Groups
    mocked_levels = mocker.MagicMock()
    mocker.patch.object(
        group_service._GroupService__xml_api,  # noqa: SLF001  # pyright: ignore[reportAttributeAccessIssue]
        "make_xml_request",
        mocked_levels,
    )
    return mocked_levels


@pytest.mark.parametrize(("element", "expected"), tests)
def test_get_all(
    element: ET.Element,
    expected: MetadataList[Group],
    group_service: GroupService,
    mock_groups: MagicMock,
) -> None:
    """Tests that wdadaptivepy properly parses Adaptive's exportGroups XML API response.

    Args:
        element: Adaptive's exportGroups XML API response
        expected: wdadaptivepy MetadataList of Groups
        group_service: wdadaptivepy GroupService
        mock_groups: Mocker for Adaptive's exportGroups XML API response

    """
    # Set the mock object to return a specific response
    mock_groups.return_value = element

    # Call the function that downloads data from the external service
    levels = group_service.get_all()

    # Verify that the function returns the expected data
    assert levels == expected


@pytest.mark.parametrize(
    ("element", "expected", "index_with_error", "key_with_error"),
    test_with_errors,
)
def test_get_all_with_errors(  # noqa: PLR0913
    element: ET.Element,
    expected: MetadataList[Group],
    index_with_error: int,
    key_with_error: str,
    group_service: GroupService,
    mock_groups: MagicMock,
) -> None:
    """Tests that wdadaptivepy properly parses Adaptive's exportGroups XML API response.

    Args:
        element: Adaptive's exportGroups XML API response
        expected: wdadaptivepy MetadataList of Groups
        index_with_error: the item in the MetadataList that shouldn't match
        key_with_error: the key for the property in that item that should't match
        group_service: wdadaptivepy GroupService
        mock_groups: Mocker for Adaptive's exportGroups XML API response

    """
    # Set the mock object to return a specific response
    mock_groups.return_value = element

    # Call the function that downloads data from the external service
    levels = group_service.get_all()

    # Verify that the function returns the expected data
    xml_value = getattr(levels[index_with_error], key_with_error, None)
    expected_value = getattr(expected[index_with_error], key_with_error, None)
    assert xml_value != expected_value
