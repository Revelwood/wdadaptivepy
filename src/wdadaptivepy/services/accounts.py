"""wdadaptivepy service for Adaptive's Accounts."""

from collections.abc import Sequence
from xml.etree import ElementTree as ET

from wdadaptivepy.connectors.xml_api.xml_api import XMLApi
from wdadaptivepy.models.account import Account
from wdadaptivepy.models.base import (
    MetadataWriteSuccessResponse,
    bool_to_str_true_false,
)
from wdadaptivepy.models.list import MetadataList


class AccountService:
    """Create, retrieve, and modify Adaptive Accounts.

    Attributes:
        Account: wdadaptivepy Account

    """

    def __init__(self, xml_api: XMLApi) -> None:
        """Initialize Account Service.

        Args:
            xml_api: Adaptive XMLApi

        """
        self.__xml_api = xml_api
        self.Account = Account

    def get_all(
        self,
        *,
        attributes: bool = True,
        include_attribute_value_names: bool = True,
        include_attribute_value_display_names: bool = True,
    ) -> MetadataList[Account]:
        """Retrieve all Accounts from Adaptive.

        Args:
            attributes: Include Account Attributes for each Account
            include_attribute_value_names: Include Name for each Account
            include_attribute_value_display_names: Include Display Name for each Account

        Returns:
            wdadaptivepy Accounts

        """
        include = ET.Element(
            "include",
            attrib={
                "attributes": str(bool_to_str_true_false(attributes)),
                "include_attribute_value_names": str(
                    bool_to_str_true_false(include_attribute_value_names),
                ),
                "include_attribute_value_display_names": str(
                    bool_to_str_true_false(include_attribute_value_display_names),
                ),
            },
        )

        response = self.__xml_api.make_xml_request(
            method="exportAccounts",
            payload=include,
        )
        return MetadataList[Account](Account.from_xml(xml=response))

    def preview_update(
        self,
        accounts: Sequence[Account],
        *,
        hide_password: bool = True,
    ) -> ET.Element:
        """Generate Account update XML API call for review prior to sending to Adaptive.

        Args:
            accounts: wdadaptivepy Accounts to update
            hide_password: Prevent password from being displayed

        Returns:
            XML API body

        """
        method, accounts_to_update = self.__build_update_payload(accounts=accounts)

        return self.__xml_api.preview_xml_request(
            method=method,
            payload=accounts_to_update,
            hide_password=hide_password,
        )

    def update(  # noqa: PLR0912, PLR0915
        self,
        accounts: Sequence[Account],
    ) -> MetadataWriteSuccessResponse:
        """Update Adaptive Accounts via XML API updateAccounts.

        Args:
            accounts: wdadaptivepy Accounts to update

        Returns:
            Updated Accounts from Adaptive

        """
        method, accounts_to_update = self.__build_update_payload(accounts=accounts)

        response = self.__xml_api.make_xml_request(
            method=method,
            payload=accounts_to_update,
        )

        success_text = response.get("success")
        if success_text is None:
            raise ValueError
        success = success_text == "true"
        messages = response.findall(".//messages")
        returned_messages: dict[str, list[str]] = {}
        for message in messages:
            message_type = message.get("type")
            message_text = message.text
            if message_type is None:
                raise RuntimeError
            if message_text is None:
                raise RuntimeError
            if message_type not in returned_messages:
                returned_messages["message_key"] = []
            returned_messages["message_key"].append(message_text)

        returned_accounts = Account.from_xml(response)
        updated_accounts = MetadataList[Account]()
        errored_accounts: dict[str, MetadataList[Account]] = {}
        for returned_account in returned_accounts:
            if not any(returned_account.id == account.id for account in accounts):
                raise RuntimeError
            account_xml = response.find(f".//account[@id='{returned_account.id}']")
            if account_xml is None:
                raise RuntimeError
            account_status = account_xml.get("status")
            if account_status in ["success", "updated"]:
                updated_accounts.append(returned_account)
            elif account_status in ["error"]:
                account_error_message = account_xml.get("message")
                if account_error_message is None:
                    raise ValueError
                if account_error_message not in errored_accounts:
                    errored_accounts[account_error_message] = MetadataList[Account]()
                if returned_account not in errored_accounts[account_error_message]:
                    errored_accounts[account_error_message].append(returned_account)
            elif account_status not in [""]:
                raise RuntimeError

            for attribute in returned_account.adaptive_attributes:
                attribute_xml = account_xml.find(
                    f".//attribute[@id'{attribute.attribute_id}'"
                )
                if attribute_xml is None:
                    raise RuntimeError
                attribute_status = attribute_xml.get("status")
                if attribute_status in ["success", "updated"]:
                    if returned_account not in updated_accounts:
                        updated_accounts.append(returned_account)
                elif attribute_status in ["error"]:
                    if returned_account in updated_accounts:
                        updated_accounts.remove(returned_account)
                    attribute_error_message = attribute_xml.get("message")
                    if attribute_error_message is None:
                        raise ValueError
                    if attribute_error_message not in errored_accounts:
                        errored_accounts[attribute_error_message] = MetadataList[
                            Account
                        ]()
                    if (
                        returned_account
                        not in errored_accounts[attribute_error_message]
                    ):
                        errored_accounts[attribute_error_message].append(
                            returned_account
                        )

        return MetadataWriteSuccessResponse(
            success=success,
            messages=returned_messages,
            xml=response,
            modified=updated_accounts,
            all=returned_accounts,
        )

    def __build_update_payload(
        self, accounts: Sequence[Account]
    ) -> tuple[str, ET.Element]:
        for account in accounts:
            if account.id is None or account.id <= 0:
                raise ValueError
            parent = account.adaptive_parent
            while parent is not None:
                if parent.id is None or account.id <= 0:
                    raise ValueError
                parent = parent.adaptive_parent
            for attribute in account.adaptive_attributes:
                if attribute.name is None or attribute.name == "":
                    raise ValueError

        return ("updateAccounts", Account.to_xml("update", accounts))

    def from_json(self, data: str) -> MetadataList[Account]:
        """Convert JSON data to MetadataList of Accounts.

        Args:
            data: JSON Data

        Returns:
            MetadataList of Accounts

        """
        return MetadataList[Account](Account.from_json(data=data))

    def from_dict(self, data: Sequence[dict] | dict) -> MetadataList[Account]:
        """Convert Python Dictionary to MetadataList of Accounts.

        Args:
            data: Python Dictionary

        Returns:
            MetadataList of Accounts

        """
        return MetadataList[Account](Account.from_dict(data=data))
