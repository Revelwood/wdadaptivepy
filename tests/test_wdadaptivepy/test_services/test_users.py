"""Tests for wdadaptivepy's service for Adaptive's Users."""

# Code using pytest-mock
from datetime import datetime
from unittest.mock import MagicMock
from xml.etree import ElementTree as ET

import pytest
from pytest_mock import MockerFixture

from wdadaptivepy.connectors.xml_api.xml_api import XMLApi
from wdadaptivepy.models import (
    MetadataList,
    User,
)
from wdadaptivepy.models.user import Subscription
from wdadaptivepy.services import UserService

tests: list[tuple[ET.Element, MetadataList[User]]] = []
test_with_errors: list[tuple[ET.Element, MetadataList[User], int, str]] = []

# Create Users
u19 = User(
    id=19,
    guid="B9ADBCB81AA2F9BAE040307F02092C2E",
    login="analytica@fakecompany.com",
    email="",
    name="Anna Analyzer",
    permission_set_ids=[3],
    time_zone="US/Pacific",
    position="Implementer",
    homepage="Welcome",
    created_date=datetime(  # NOQA: DTZ001
        year=2020,
        month=6,
        day=26,
        hour=7,
        minute=56,
        second=0,
        microsecond=0,
    ),
    last_login=datetime(  # NOQA: DTZ001
        year=2020,
        month=6,
        day=26,
        hour=8,
        minute=48,
        second=34,
        microsecond=0,
    ),
    failed_attempts=0,
    locked=False,
    subscriptions=Subscription(
        no_subscriptions=False,
        customer_news_letter=False,
        customer_webinars=False,
        education_training=False,
        local_events=False,
        partner_news_letter=False,
        partner_webinars=False,
        new_products_and_enhancements=False,
        surveys=False,
        sysem_alerts_and_updates=True,
        user_groups=False,
    ),
)
u123 = User(
    id=123,
    guid="AAFF5218D55ABB9234660001BEC117A9",
    login="randomuser@fakecompany.com",
    email="randomuser@fakecompany.com",
    name="J. Random User",
    permission_set_ids=[2],
    group_ids=[304, 1, 101, 102],
    time_zone="US/Pacific",
    alternate_email="randomuser@fakecompany.com",
    position="Director FP&A",
    homepage="Welcome",
    created_date=datetime(  # NOQA: DTZ001
        year=2020,
        month=6,
        day=26,
        hour=7,
        minute=56,
        second=0,
        microsecond=0,
    ),
    last_login=datetime(  # NOQA: DTZ001
        year=2024,
        month=7,
        day=19,
        hour=4,
        minute=56,
        second=32,
        microsecond=0,
    ),
    failed_attempts=0,
    locked=False,
    subscriptions=Subscription(
        no_subscriptions=False,
        customer_news_letter=False,
        customer_webinars=False,
        education_training=False,
        local_events=False,
        partner_news_letter=False,
        partner_webinars=False,
        new_products_and_enhancements=False,
        surveys=False,
        sysem_alerts_and_updates=True,
        user_groups=False,
    ),
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
      <user id="19" login="analytica@fakecompany.com" email="" name="Anna Analyzer" permissionSetIds="3" guid="B9ADBCB81AA2F9BAE040307F02092C2E" timeZone="US/Pacific" position="Implementer" homepage="Welcome" createdDate="2020-06-26 07:56:00.0" lastLogin="2020-06-26 08:48:34.0" failedAttempts="0" locked="false">
        <subscriptions nosubscriptions="0" customerNewsLetter="0" customerWebinars="0" educationTraining="0" localEvents="0" partnerNewsLetter="0" partnerWebinars="0" newProductsAndEnhancements="0" surveys="0" systemAlertsAndUpdates="1" userGroups="0" />
      </user>
      <user id="123" login="randomuser@fakecompany.com" email="randomuser@fakecompany.com" name="J. Random User" permissionSetIds="2" guid="AAFF5218D55ABB9234660001BEC117A9" timeZone="US/Pacific" groupIds="304,1,101,102" alternateEmail="randomuser@fakecompany.com" position="Director FP&amp;A" homepage="Welcome" createdDate="2020-06-26 07:56:00.0" lastLogin="2024-07-19 04:56:32.0" failedAttempts="0" locked="false">
        <subscriptions nosubscriptions="0" customerNewsLetter="0" customerWebinars="0" educationTraining="0" localEvents="0" partnerNewsLetter="0" partnerWebinars="0" newProductsAndEnhancements="0" surveys="0" systemAlertsAndUpdates="1" userGroups="0" />
      </user>
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
