"""wdadaptivepy service for Adaptive's Levels."""

from collections.abc import Sequence
from xml.etree import ElementTree as ET

from wdadaptivepy.connectors.xml_api.xml_api import XMLApi
from wdadaptivepy.models.base import bool_to_str_true_false
from wdadaptivepy.models.level import Level
from wdadaptivepy.models.list import MetadataList


class LevelService:
    """Create, retrieve, and modify Adaptive Levels.

    Attributes:
        Level: wdadaptivepylevel

    """

    def __init__(self, xml_api: XMLApi) -> None:
        """Initialize LevelService.

        Args:
            xml_api: wdadaptivepy XMLApi

        """
        self.__xml_api = xml_api
        self.Level = Level

    def get_all(self, *, display_name_enabled: bool = True) -> MetadataList[Level]:
        """Retrieve all Levels from Adaptive.

        Args:
            display_name_enabled: Adaptive Display Name Enabled

        Returns:
            adaptive Levels

        """
        include = ET.Element(
            "include",
            attrib={
                "displayNameEnabled": str(bool_to_str_true_false(display_name_enabled)),
            },
        )

        response = self.__xml_api.make_xml_request(
            method="exportLevels",
            payload=include,
        )
        return MetadataList[Level](Level.from_xml(xml=response))

    def preview_update(
        self,
        levels: Sequence[Level],
        *,
        hide_password: bool = True,
    ) -> ET.Element:
        """Generate Level update XML API call for review.

        Args:
            levels: wdadaptivepy Levels to update
            hide_password: Prevent password from being displayed

        Returns:
            XML API body

        """
        updated_levels = Level.to_xml("update", levels)
        return self.__xml_api.preview_xml_request(
            method="importLevels",
            payload=updated_levels,
            hide_password=hide_password,
        )

    def from_json(self, data: str) -> MetadataList[Level]:
        """Convert JSON to MetadataList of Levels.

        Args:
            data: JSON string

        Returns:
            MetadataList of Levels

        """
        return MetadataList[Level](Level.from_json(data=data))

    def from_dict(self, data: Sequence[dict] | dict) -> MetadataList[Level]:
        """Convert Python Dictionary to MetadataList of Levels.

        Args:
            data: Python Dictionary

        Returns:
            MetadataList of Levels

        """
        return MetadataList[Level](Level.from_dict(data=data))
