"""wdadaptivepy service for Adaptive's Versions."""

from collections.abc import Sequence
from xml.etree import ElementTree as ET

from wdadaptivepy.connectors.xml_api.xml_api import XMLApi
from wdadaptivepy.models.base import bool_to_str_true_false
from wdadaptivepy.models.list import MetadataList
from wdadaptivepy.models.version import Version


class VersionService:
    """Create, retrieve, and modify Adaptive Versions.

    Attributes:
        Version: wdadaptivepy Version

    """

    def __init__(self, xml_api: XMLApi) -> None:
        """Initialize VersionService.

        Args:
            xml_api: wdadaptivepy XMLApi

        """
        self.__xml_api = xml_api
        self.Version = Version

    def get_all(
        self,
        *,
        scenarios: bool = False,
        currency_versions: bool = False,
    ) -> MetadataList[Version]:
        """Retrieve all Versions from Adaptive.

        Args:
            scenarios: Adaptive Scenarios
            currency_versions: Adaptive Currency Versions

        Returns:
            adaptive Versions

        """
        include = ET.Element(
            "include",
            attrib={
                "scenarios": str(bool_to_str_true_false(scenarios)),
                "currencyVersions": str(bool_to_str_true_false(currency_versions)),
            },
        )

        response = self.__xml_api.make_xml_request(
            method="exportVersions",
            payload=include,
        )
        return MetadataList[Version](Version.from_xml(xml=response))

    def preview_update(
        self,
        versions: Sequence[Version],
        *,
        hide_password: bool = True,
    ) -> ET.Element:
        """Generate Currency update XML API call for review.

        Args:
            versions: wdadaptivepy Versions to update
            hide_password: Prevent password from being displayed

        Returns:
            XML API body

        """
        updated_versions = Version.to_xml("update", versions)
        return self.__xml_api.preview_xml_request(
            method="importVersions",
            payload=updated_versions,
            hide_password=hide_password,
        )

    def from_json(self, data: str) -> MetadataList[Version]:
        """Convert JSON to MetadataList of Versions.

        Args:
            data: JSON string

        Returns:
            MetadataList of Versions

        """
        return MetadataList[Version](Version.from_json(data=data))

    def from_dict(self, data: Sequence[dict] | dict) -> MetadataList[Version]:
        """Convert Python Dictionary to MetadataList of Versions.

        Args:
            data: Python Dictionary

        Returns:
            MetadataList of Versions

        """
        return MetadataList[Version](Version.from_dict(data=data))
