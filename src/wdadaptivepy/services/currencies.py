"""wdadaptivepy service for Adaptive's Currencies."""

from collections.abc import Sequence
from xml.etree import ElementTree as ET

from wdadaptivepy.connectors.xml_api.xml_api import XMLApi
from wdadaptivepy.models.currency import Currency
from wdadaptivepy.models.list import MetadataList


class CurrencyService:
    """Create, retrieve, and modify Adaptive Currencies.

    Attributes:
        Currency: wdadaptivepy Currency

    """

    def __init__(self, xml_api: XMLApi) -> None:
        """Initialize CurrencyService.

        Args:
            xml_api: wdadaptivepy XMLApi

        """
        self.__xml_api = xml_api
        self.Currency = Currency

    def get_all(self) -> MetadataList[Currency]:
        """Retrieve all Currencies from Adaptive.

        Returns:
            adaptive Currencies

        """
        response = self.__xml_api.make_xml_request(
            method="exportActiveCurrencies",
            payload=None,
        )
        return MetadataList[Currency](Currency.from_xml(xml=response))

    def preview_update(
        self,
        currencies: Sequence[Currency],
        *,
        hide_password: bool = True,
    ) -> ET.Element:
        """Generate Currency update XML API call for review.

        Args:
            currencies: wdadaptivepy Currencies to update
            hide_password: Prevent password from being displayed

        Returns:
            XML API body

        """
        updated_currencies = Currency.to_xml("update", currencies)
        # ET.indent(updated_currencies)
        # with open("test_currencies.xml", "w", encoding="utf-8") as fp:
        #     fp.write(ET.tostring(updated_currencies, encoding="unicode"))
        return self.__xml_api.preview_xml_request(
            method="importCurrencies",
            payload=updated_currencies,
            hide_password=hide_password,
        )

    def from_json(self, data: str) -> MetadataList[Currency]:
        """Convert JSON to MetadataList of Currencies.

        Args:
            data: JSON string

        Returns:
            MetadataList of Currencies

        """
        return MetadataList[Currency](Currency.from_json(data=data))

    def from_dict(self, data: Sequence[dict] | dict) -> MetadataList[Currency]:
        """Convert Python Dictionary to MetadataList of Currencies.

        Args:
            data: Python Dictionary

        Returns:
            MetadataList of Currencies

        """
        return MetadataList[Currency](Currency.from_dict(data=data))
