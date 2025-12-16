"""wdadaptivepy service for Adaptive's Permission Sets."""

from collections.abc import Sequence
from xml.etree import ElementTree as ET

from wdadaptivepy.connectors.xml_api.xml_api import XMLApi
from wdadaptivepy.models.list import MetadataList
from wdadaptivepy.models.permission_set import PermissionSet


class PermissionSetService:
    """Create, retrieve, and modify Adaptive Permission Sets.

    Attributes:
        PermissionSet: wdadaptivepy Permission Set

    """

    def __init__(self, xml_api: XMLApi) -> None:
        """Initialize PermissionSetService.

        Args:
            xml_api: wdadaptivepy XMLApi

        """
        self.__xml_api = xml_api
        self.PermissionSet = PermissionSet

    def get_all(self) -> MetadataList[PermissionSet]:
        """Retrieve all Permission Sets from Adaptive.

        Returns:
            adaptive Permission Sets

        """
        response = self.__xml_api.make_xml_request(
            method="exportPermissionSets",
            payload=None,
        )
        return MetadataList[PermissionSet](PermissionSet.from_xml(xml=response))

    def preview_update(
        self,
        permission_sets: Sequence[PermissionSet],
        *,
        hide_password: bool = True,
    ) -> ET.Element:
        """Generate Permission Set update XML API call for review.

        Args:
            permission_sets: wdadaptivepy Permission Sets to update
            hide_password: Prevent password from being displayed

        Returns:
            XML API body

        """
        updated_permission_sets = PermissionSet.to_xml("update", permission_sets)
        return self.__xml_api.preview_xml_request(
            method="importPermissionSets",
            payload=updated_permission_sets,
            hide_password=hide_password,
        )

    def from_json(self, data: str) -> MetadataList[PermissionSet]:
        """Convert JSON to MetadataList of Permission Sets.

        Args:
            data: JSON string

        Returns:
            MetadataList of Permission Sets

        """
        return MetadataList[PermissionSet](PermissionSet.from_json(data=data))

    def from_dict(self, data: Sequence[dict] | dict) -> MetadataList[PermissionSet]:
        """Convert Python Dictionary to MetadataList of Permission Sets.

        Args:
            data: Python Dictionary

        Returns:
            MetadataList of Permission Sets

        """
        return MetadataList[PermissionSet](PermissionSet.from_dict(data=data))
