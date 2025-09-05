"""Tests for wdadaptivepy's service for Adaptive's Users."""

# Code using pytest-mock
from unittest.mock import MagicMock
from xml.etree import ElementTree as ET

import pytest
from pytest_mock import MockerFixture

from wdadaptivepy.connectors.xml_api.xml_api import XMLApi
from wdadaptivepy.models import (
    MetadataList,
    User,
)
from wdadaptivepy.services import UserService

tests: list[tuple[ET.Element, MetadataList[User]]] = []
test_with_errors: list[tuple[ET.Element, MetadataList[User], int, str]] = []

# Create Users
u19 = User(
    id=19,
    guid="B9ADBCB81AA2F9BAE040307F02092C2E",
    login="analytica@fakecompany.com",
    email="analytica@fakecompany.com",
    name="Anna Analyzer",
    permission_set_ids=[3],
    time_zone="US/Pacific",
)
u123 = User(
    id=123,
    guid="AAFF5218D55ABB9234660001BEC117A9",
    login="randomuser@fakecompany.com",
    email="randomuser@fakecompany.com",
    name="J. Random User",
    permission_set_ids=[2],
    time_zone="US/Pacific",
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
   <users seqNo="55">
     <user id="19" guid="B9ADBCB81AA2F9BAE040307F02092C2E" login="analytica@fakecompany.com" email="analytica@fakecompany.com" name="Anna Analyzer" permissionSetIds="3" timeZone="US/Pacific"/>
     <user id="123" guid="AAFF5218D55ABB9234660001BEC117A9" login="randomuser@fakecompany.com" email="randomuser@fakecompany.com" name="J. Random User" permissionSetIds="2" timeZone="US/Pacific"/>
   </users>
</output>
</response> """)  # noqa: E501

tests.append(
    (
        xml2,
        MetadataList([u19, u123]),
    ),
)


# From here down, we're using the original testing methodology
@pytest.fixture
def user_service() -> UserService:
    """Fixture for wdadaptivepy's User Service.

    Returns:
        wdadaptivepy UserService

    """
    xml_api_instance = XMLApi("", "")
    return UserService(xml_api=xml_api_instance)


@pytest.fixture
def mock_users(
    mocker: MockerFixture,
    user_service: UserService,
) -> ET.Element:
    """Mock Adaptive's response from exportUsers XML API.

    Args:
        mocker: pytest's mocker
        user_service: wdadaptivepy UserService to mock

    Returns:
        XML Element

    """
    # Create a mock object for the Users
    mocked_levels = mocker.MagicMock()
    mocker.patch.object(
        user_service._UserService__xml_api,  # noqa: SLF001  # pyright: ignore[reportAttributeAccessIssue]
        "make_xml_request",
        mocked_levels,
    )
    return mocked_levels


@pytest.mark.parametrize(("element", "expected"), tests)
def test_get_all(
    element: ET.Element,
    expected: MetadataList[User],
    user_service: UserService,
    mock_users: MagicMock,
) -> None:
    """Tests that wdadaptivepy properly parses Adaptive's exportUsers XML API response.

    Args:
        element: Adaptive's exportUsers XML API response
        expected: wdadaptivepy MetadataList of Users
        user_service: wdadaptivepy UserService
        mock_users: Mocker for Adaptive's exportUsers XML API response

    """
    # Set the mock object to return a specific response
    mock_users.return_value = element

    # Call the function that downloads data from the external service
    levels = user_service.get_all()

    # Verify that the function returns the expected data
    assert levels == expected


@pytest.mark.parametrize(
    ("element", "expected", "index_with_error", "key_with_error"),
    test_with_errors,
)
def test_get_all_with_errors(  # noqa: PLR0913
    element: ET.Element,
    expected: MetadataList[User],
    index_with_error: int,
    key_with_error: str,
    user_service: UserService,
    mock_users: MagicMock,
) -> None:
    """Tests that wdadaptivepy properly parses Adaptive's exportUsers XML API response.

    Args:
        element: Adaptive's exportUsers XML API response
        expected: wdadaptivepy MetadataList of Users
        index_with_error: the item in the MetadataList that shouldn't match
        key_with_error: the key for the property in that item that should't match
        user_service: wdadaptivepy UserService
        mock_users: Mocker for Adaptive's exportUsers XML API response

    """
    # Set the mock object to return a specific response
    mock_users.return_value = element

    # Call the function that downloads data from the external service
    levels = user_service.get_all()

    # Verify that the function returns the expected data
    xml_value = getattr(levels[index_with_error], key_with_error, None)
    expected_value = getattr(expected[index_with_error], key_with_error, None)
    assert xml_value != expected_value
