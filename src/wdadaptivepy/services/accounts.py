"""wdadaptivepy service for Adaptive's Accounts."""

from collections.abc import Sequence
from xml.etree import ElementTree as ET

from wdadaptivepy.connectors.xml_api.xml_api import XMLApi
from wdadaptivepy.models.account import Account
from wdadaptivepy.models.base import bool_to_str_true_false
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
        updated_accounts = Account.to_xml("update", accounts)
        # ET.indent(updated_accounts)
        # with open("test_accounts.xml", "w", encoding="utf-8") as fp:
        #     fp.write(ET.tostring(updated_accounts, encoding="unicode"))
        return self.__xml_api.preview_xml_request(
            method="importAccounts",
            payload=updated_accounts,
            hide_password=hide_password,
        )

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
