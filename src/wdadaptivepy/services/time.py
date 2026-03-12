"""wdadaptivepy service for Adaptive's Time."""

from collections.abc import Sequence
from xml.etree import ElementTree as ET

from wdadaptivepy.connectors.xml_api.xml_api import XMLApi
from wdadaptivepy.models.base import bool_to_str_one_zero
from wdadaptivepy.models.list import MetadataList
from wdadaptivepy.models.time import Period, Stratum, Time


class TimeService:
    """Create, retrieve, and modify Adaptive Time.

    Attributes:
        Time: wdadaptivepy Time
        Period: wdadaptivepy Period
        Stratum: wdadaptivepy Stratum

    """

    def __init__(self, xml_api: XMLApi) -> None:
        """Initialize TimeService.

        Args:
            xml_api: wdadaptivepy XMLApi

        """
        self.__xml_api = xml_api
        self.Time = Time
        self.Period = Period
        self.Stratum = Stratum

    def get_all(
        self,
        *,
        include_all_locales: bool = False,
        include_legacy_information: bool = False,
    ) -> MetadataList[Time]:
        """Retrieve all Time from Adaptive.

        Args:
            include_all_locales: Adaptive Include All Locales
            include_legacy_information: Adaptive Include Legacy Information

        Returns:
            adaptive Time

        """
        options = ET.Element(
            "options",
            attrib={
                "includeAllLocales": str(bool_to_str_one_zero(include_all_locales)),
                "includeLegacyInformation": str(
                    bool_to_str_one_zero(include_legacy_information),
                ),
            },
        )

        response = self.__xml_api.make_xml_request(method="exportTime", payload=options)
        return MetadataList[Time](Time.from_xml(xml=response))

    def preview_update(
        self,
        times: Sequence[Time],
        *,
        hide_password: bool = True,
    ) -> ET.Element:
        """Generate Time update XML API call for review.

        Args:
            times: wdadaptivepy Time to update
            hide_password: Prevent password from being displayed

        Returns:
            XML API body

        """
        updated_times = Time.to_xml("update", times)
        return self.__xml_api.preview_xml_request(
            method="importTime",
            payload=updated_times,
            hide_password=hide_password,
        )

    def from_json(self, data: str) -> MetadataList[Time]:
        """Convert JSON to MetadataList of Time.

        Args:
            data: JSON string

        Returns:
            MetadataList of Time

        """
        return MetadataList[Time](Time.from_json(data=data))

    def from_dict(self, data: Sequence[dict] | dict) -> MetadataList[Time]:
        """Convert Python Dictionary to MetadataList of Time.

        Args:
            data: Python Dictionary

        Returns:
            MetadataList of Time

        """
        return MetadataList[Time](Time.from_dict(data=data))
