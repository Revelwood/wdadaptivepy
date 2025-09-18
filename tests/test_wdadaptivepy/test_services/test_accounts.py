"""Tests for wdadaptivepy's service for Adaptive's Accounts."""

# Code using pytest-mock
from unittest.mock import MagicMock
from xml.etree import ElementTree as ET

import pytest
from pytest_mock import MockerFixture

from wdadaptivepy.connectors.xml_api.xml_api import XMLApi
from wdadaptivepy.models import Account, MetadataList
from wdadaptivepy.services import AccountService

tests: list[tuple[ET.Element, MetadataList[Account]]] = []
test_with_errors: list[tuple[ET.Element, MetadataList[Account], int, str]] = []


# TEST 1 # Empty xml returns empty MetadataList
xml1 = ET.fromstring("""<?xml version='1.0' encoding='UTF-8'?>
<response success='true'>
  <output>
  </output>
</response>""")
tests.append((xml1, MetadataList([])))


# TODO: Change this to the one from the docs  # noqa: FIX002, TD002, TD003
# TEST 4 ######################################################################
xml4 = ET.fromstring("""<?xml version='1.0' encoding='UTF-8'?>
<response success='true'>
  <output>
    <accounts seqNo='0' displayNameType='NAME'>
      <account id='124' name='hello'/>
    </accounts>
  </output>
</response>""")
tests.append((xml4, MetadataList([Account(id=124, name="hello")])))


# From here down, we're using the original testing methodology
@pytest.fixture
def account_service() -> AccountService:
    """Fixture for wdadaptivepy's Account Service.

    Returns:
        wdadaptivepy AccountService

    """
    xml_api_instance = XMLApi("", "")
    return AccountService(xml_api=xml_api_instance)


@pytest.fixture
def mock_accounts(mocker: MockerFixture, account_service: AccountService) -> ET.Element:
    """Mock Adaptive's response from exportAccounts XML API.

    Args:
        mocker: pytest's mocker
        account_service: wdadaptivepy AccountService to mock

    Returns:
        XML Element

    """
    # Create a mock object for the Accounts
    mocked_accounts = mocker.MagicMock()
    mocker.patch.object(
        account_service._AccountService__xml_api,  # noqa: SLF001  # pyright: ignore[reportAttributeAccessIssue]
        "make_xml_request",
        mocked_accounts,
    )
    return mocked_accounts


@pytest.mark.parametrize(("element", "expected"), tests)
def test_get_all(
    element: ET.Element,
    expected: MetadataList[Account],
    account_service: AccountService,
    mock_accounts: MagicMock,
) -> None:
    """Tests that wdadaptivepy properly parses Adaptive's exportAccounts XML API response.

    Args:
        element: Adaptive's exportAccounts XML API response
        expected: wdadaptivepy MetadataList of Accounts
        account_service: wdadaptivepy AccountService
        mock_accounts: Mocker for Adaptive's exportAccounts XML API response

    """
    # Set the mock object to return a specific response
    mock_accounts.return_value = element

    # Call the function that downloads data from the external service
    accounts = account_service.get_all()

    # Verify that the function returns the expected data
    assert accounts == expected


@pytest.mark.parametrize(
    ("element", "expected", "index_with_error", "key_with_error"),
    test_with_errors,
)
def test_get_all_with_errors(  # noqa: PLR0913
    element: ET.Element,
    expected: MetadataList[Account],
    index_with_error: int,
    key_with_error: str,
    account_service: AccountService,
    mock_accounts: MagicMock,
) -> None:
    """Tests that wdadaptivepy properly parses Adaptive's exportAccounts API response.

    Args:
        element: Adaptive's exportAccounts XML API response
        expected: wdadaptivepy MetadataList of Accounts
        index_with_error: the item in the MetadataList that shouldn't match
        key_with_error: the key for the property in that item that should't match
        account_service: wdadaptivepy AccountService
        mock_accounts: Mocker for Adaptive's exportAccounts XML API response

    """
    # Set the mock object to return a specific response
    mock_accounts.return_value = element

    # Call the function that downloads data from the external service
    accounts = account_service.get_all()

    # Verify that the function returns the expected data
    xml_value = getattr(accounts[index_with_error], key_with_error, None)
    expected_value = getattr(expected[index_with_error], key_with_error, None)
    assert xml_value != expected_value
