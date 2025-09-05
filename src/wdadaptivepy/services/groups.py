"""wdadaptivepy service for Adaptive's Groups."""

from collections.abc import Sequence
from xml.etree import ElementTree as ET

from wdadaptivepy.connectors.xml_api.xml_api import XMLApi
from wdadaptivepy.models.group import Group
from wdadaptivepy.models.list import MetadataList


class GroupService:
    """Create, retrieve, and modify Adaptive Grups.

    Attributes:
        Group: wdadaptivepy Group

    """

    def __init__(self, xml_api: XMLApi) -> None:
        """Initialize GroupService.

        Args:
            xml_api: wdadaptivepy XMLApi

        """
        self.__xml_api = xml_api
        self.Group = Group

    def get_all(self) -> MetadataList[Group]:
        """Retrieve all Groups from Adaptive.

        Returns:
            adaptive Groups

        """
        response = self.__xml_api.make_xml_request(method="exportGroups", payload=None)
        return MetadataList[Group](Group.from_xml(xml=response))

    def preview_update(
        self,
        groups: Sequence[Group],
        *,
        hide_password: bool = True,
    ) -> ET.Element:
        """Generate Group update XML API call for review.

        Args:
            groups: wdadaptivepy Groups to update
            hide_password: Prevent password from being displayed

        Returns:
           XML API body

        """
        updated_groups = Group.to_xml("update", groups)
        # ET.indent(updated_groups)
        # with open("test_groups.xml", "w", encoding="utf-8") as fp:
        #     fp.write(ET.tostring(updated_groups, encoding="unicode"))
        return self.__xml_api.preview_xml_request(
            method="importGroups",
            payload=updated_groups,
            hide_password=hide_password,
        )

    def from_json(self, data: str) -> MetadataList[Group]:
        """Convert JSON to MetadataList of Groups.

        Args:
            data: JSON string

        Returns:
            MetadataList of Groups

        """
        return MetadataList[Group](Group.from_json(data=data))

    def from_dict(self, data: Sequence[dict] | dict) -> MetadataList[Group]:
        """Convert Python Dictionary to MetadataList of Groups.

        Args:
            data: Pytho Dictionary

        Returns:
            MetadataList of Groups

        """
        return MetadataList[Group](Group.from_dict(data=data))
