"""Tests for wdadaptivepy's service for Adaptive's Accounts."""

# Code using pytest-mock
from collections.abc import Sequence
from unittest.mock import MagicMock
from xml.etree import ElementTree as ET

import pytest
from pytest_mock import MockerFixture

from wdadaptivepy.connectors.xml_api.xml_api import XMLApi
from wdadaptivepy.models import Account, MetadataList
from wdadaptivepy.models.base import MetadataAttribute, MetadataWriteSuccessResponse
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
    """Tests wdadaptivepy properly parses Adaptive's exportAccounts XML API response.

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


update_accounts: list[tuple[MetadataList[Account], ET.Element]] = []
first_account_attribute = MetadataAttribute(
    attribute_id=1231,
    name="First Account Attribute",
    value_id=12311,
    value="First Account Attribute First Value",
)
second_account_attribute = MetadataAttribute(
    attribute_id=1232,
    name="Second Account Attribute",
    value_id=12321,
    value="Second Account Attribute First Value",
)
first_account = Account(
    id=12341,
    code="First_Account_Code",
    name="First Account Name",
    account_type_code="A",
    description="First Account Description",
    short_name="First Account",
)
second_account = Account(
    id=12342,
    code="Second_Account_Code",
    name="Second Account Name",
    account_type_code="A",
    description="Second Account Description",
    short_name="Second Account",
)
third_account = Account(
    id=12343,
    code="Third_Account_Code",
    name="Third Account Name",
    account_type_code="A",
    description="Third Account Description",
    short_name="Third Account",
)
fourth_account = Account(
    id=12344,
    code="Fourth_Account_Code",
    name="Fourth Account Name",
    account_type_code="A",
    description="Fourth Account Description",
    short_name="Fourth Account",
)
fifth_account = Account(
    id=12345,
    code="Fifth_Account_Code",
    name="Fifth Account Name",
    account_type_code="A",
    description="Fifth Account Description",
    short_name="Fifth Account",
)
sixth_account = Account(
    id=12346,
    code="Sixth_Account_Code",
    name="Sixth Account Name",
    account_type_code="A",
    description="Sixth Account Description",
    short_name="Sixth Account",
)
seventh_account = Account(
    id=12347,
    code="Seventh_Account_Code",
    name="Seventh Account Name",
    account_type_code="A",
    description="Seventh Account Description",
    short_name="Seventh Account",
)
eighth_account = Account(
    id=12348,
    code="Eighth_Account_Code",
    name="Eighth Account Name",
    account_type_code="A",
    description="Eighth Account Description",
    short_name="Eighth Account",
)
ninth_account = Account(
    id=12349,
    code="Ninth_Account_Code",
    name="Ninth Account Name",
    account_type_code="A",
    description="Ninth Account Description",
    short_name="Ninth Account",
)
seventh_account.set_adaptive_parent(second_account)
sixth_account.set_adaptive_parent(fourth_account)
fifth_account.set_adaptive_parent(fourth_account)
fourth_account.set_adaptive_parent(third_account)
third_account.set_adaptive_parent(second_account)
second_account.set_adaptive_parent(first_account)

fifth_account.set_adaptive_attribute(first_account_attribute)
fifth_account.set_adaptive_attribute(second_account_attribute)
eighth_account.set_adaptive_attribute(first_account_attribute)
eighth_account.set_adaptive_attribute(second_account_attribute)
ninth_account.set_adaptive_attribute(second_account_attribute)
ninth_account.remove_adaptive_attribute(second_account_attribute)

update_accounts.append(
    (
        MetadataList(
            [
                eighth_account,
                seventh_account,
                sixth_account,
                ninth_account,
                first_account,
                second_account,
                third_account,
                fourth_account,
                fifth_account,
            ]
        ),
        ET.fromstring(
            """<accounts>"""
            """    <account id="12348" code="Eighth_Account_Code" name="Eighth Account Name" accountTypeCode="A" description="Eighth Account Description" shortName="Eighth Account">"""  # noqa: E501
            """        <attribute name="First Account Attribute" value="First Account Attribute First Value" />"""  # noqa: E501
            """        <attribute name="Second Account Attribute" value="Second Account Attribute First Value" />"""  # noqa: E501
            """    </account>"""
            """    <account id="12349" code="Ninth_Account_Code" name="Ninth Account Name" accountTypeCode="A" description="Ninth Account Description" shortName="Ninth Account">"""  # noqa: E501
            """        <attribute name="Second Account Attribute" value="" />"""
            """    </account>"""
            """    <account id="12341" code="First_Account_Code" name="First Account Name" accountTypeCode="A" description="First Account Description" shortName="First Account">"""  # noqa: E501
            """        <account id="12342" code="Second_Account_Code" name="Second Account Name" accountTypeCode="A" description="Second Account Description" shortName="Second Account">"""  # noqa: E501
            """            <account id="12343" code="Third_Account_Code" name="Third Account Name" accountTypeCode="A" description="Third Account Description" shortName="Third Account">"""  # noqa: E501
            """                <account id="12344" code="Fourth_Account_Code" name="Fourth Account Name" accountTypeCode="A" description="Fourth Account Description" shortName="Fourth Account">"""  # noqa: E501
            """                    <account id="12346" code="Sixth_Account_Code" name="Sixth Account Name" accountTypeCode="A" description="Sixth Account Description" shortName="Sixth Account" />"""  # noqa: E501
            """                    <account id="12345" code="Fifth_Account_Code" name="Fifth Account Name" accountTypeCode="A" description="Fifth Account Description" shortName="Fifth Account">"""  # noqa: E501
            """                        <attribute name="First Account Attribute" value="First Account Attribute First Value" />"""  # noqa: E501
            """                        <attribute name="Second Account Attribute" value="Second Account Attribute First Value" />"""  # noqa: E501
            """                    </account>"""
            """                </account>"""
            """            </account>"""
            """            <account id="12347" code="Seventh_Account_Code" name="Seventh Account Name" accountTypeCode="A" description="Seventh Account Description" shortName="Seventh Account" />"""  # noqa: E501
            """        </account>"""
            """    </account>"""
            """</accounts>"""
        ),
    )
)
update_accounts.append(
    (
        MetadataList(
            [
                second_account,
                fifth_account,
                ninth_account,
            ]
        ),
        ET.fromstring(
            """<accounts>"""
            """    <account id="12341">"""
            """        <account id="12342" code="Second_Account_Code" name="Second Account Name" accountTypeCode="A" description="Second Account Description" shortName="Second Account" />"""  # noqa: E501
            """    </account>"""
            """    <account id="12344">"""
            """        <account id="12345" code="Fifth_Account_Code" name="Fifth Account Name" accountTypeCode="A" description="Fifth Account Description" shortName="Fifth Account">"""  # noqa: E501
            """            <attribute name="First Account Attribute" value="First Account Attribute First Value" />"""  # noqa: E501
            """            <attribute name="Second Account Attribute" value="Second Account Attribute First Value" />"""  # noqa: E501
            """        </account>"""
            """    </account>"""
            """    <account id="12349" code="Ninth_Account_Code" name="Ninth Account Name" accountTypeCode="A" description="Ninth Account Description" shortName="Ninth Account">"""  # noqa: E501
            """        <attribute name="Second Account Attribute" value="" />"""
            """    </account>"""
            """</accounts>"""
        ),
    )
)
update_accounts.append(
    (
        MetadataList(
            [
                third_account,
            ]
        ),
        ET.fromstring(
            """<accounts>"""
            """    <account id="12342" >"""
            """        <account id="12343" code="Third_Account_Code" name="Third Account Name" accountTypeCode="A" description="Third Account Description" shortName="Third Account" />"""  # noqa: E501
            """    </account>"""
            """</accounts>"""
        ),
    )
)
update_accounts.append(
    (
        MetadataList(
            [
                first_account,
            ]
        ),
        ET.fromstring(
            """<accounts>"""
            """    <account id="12341" code="First_Account_Code" name="First Account Name" accountTypeCode="A" description="First Account Description" shortName="First Account" />"""  # noqa: E501
            """</accounts>"""
        ),
    )
)
update_accounts.append(
    (
        MetadataList(
            [
                third_account,
            ]
        ),
        ET.fromstring(
            """<accounts>"""
            """    <account id="12342" >"""
            """        <account id="12343" code="Third_Account_Code" name="Third Account Name" accountTypeCode="A" description="Third Account Description" shortName="Third Account" />"""  # noqa: E501
            """    </account>"""
            """</accounts>"""
        ),
    )
)


@pytest.mark.parametrize(
    ("accounts", "expected"),
    update_accounts,
)
def test_update_accounts(
    accounts: Sequence[Account],
    expected: ET.Element,
    account_service: AccountService,
    mock_accounts: MagicMock,
) -> None:
    """Tests that wdadaptivepy properly builds updateAccounts API requests.

    Args:
        accounts: accounts to update
        expected: Adaptive's updateAccounts XML API request
        account_service: wdadaptivepy AccountService
        mock_accounts: Mocker for Adaptive's updateAccounts XML API request

    """
    account_service.update(accounts)
    update_kwargs = mock_accounts.call_args.kwargs
    assert update_kwargs["method"] == "updateAccounts"

    ET.indent(update_kwargs["payload"])
    ET.indent(expected)
    assert ET.tostring(update_kwargs["payload"]) == ET.tostring(expected)


test_update_accounts_response_values: list[
    tuple[MetadataList[Account], ET.Element, MetadataWriteSuccessResponse]
] = []
first_update_accounts = MetadataList[Account](
    [
        Account(id=1001, code="10001", name="Cash"),
        Account(id=1002, code="10002", name="Petty Cash"),
    ]
)
first_update_response = ET.fromstring(
    """<?xml version='1.0' encoding='UTF-8'?>"""
    """<response success="true">"""
    """    <output>"""
    """        <accounts proceedWithWarnings="0" displayNameEnabled="1">"""
    """            <account id="1001" code="10001" name="Cash" status="updated" />"""
    """            <account id="1002" code="10002" name="Petty Cash" status="" />"""
    """        </accounts>"""
    """    </output>"""
    """</response>""",
)

test_update_accounts_response_values.append(
    (
        first_update_accounts,
        first_update_response,
        MetadataWriteSuccessResponse(
            success=True,
            messages={},
            xml=first_update_response,
            modified=MetadataList[Account](
                [Account(id=1001, code="10001", name="Cash")]
            ),
            all=MetadataList[Account](
                [
                    Account(id=1001, code="10001", name="Cash"),
                    Account(id=1002, code="10002", name="Petty Cash"),
                ]
            ),
        ),
    )
)


@pytest.mark.parametrize(
    ("accounts", "element", "expected"), test_update_accounts_response_values
)
def test_update_accounts_response(
    accounts: Sequence[Account],
    element: ET.Element,
    expected: MetadataWriteSuccessResponse,
    account_service: AccountService,
    mock_accounts: MagicMock,
) -> None:
    """Tests wdadaptivepy properly parses Adaptive's updateAccounts XML API response.

    Args:
        accounts: Accounts to update
        element: Adaptive's updateAccounts XML API response
        expected: wdadaptivepy Metadata Writeback Success Response
        account_service: wdadaptivepy AccountService
        mock_accounts: Mocker for Adaptive's updateAccounts XML API response

    """
    mock_accounts.return_value = element
    update_response = account_service.update(accounts)

    assert update_response == expected
