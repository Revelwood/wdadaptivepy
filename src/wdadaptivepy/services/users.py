"""wdadaptivepy service for Adaptive's Users."""

from collections.abc import Sequence
from xml.etree import ElementTree as ET

from wdadaptivepy.connectors.xml_api.xml_api import XMLApi
from wdadaptivepy.models.base import bool_to_str_true_false
from wdadaptivepy.models.list import MetadataList
from wdadaptivepy.models.user import User


class UserService:
    """Create, retrieve, and modify Adaptive Users.

    Attributes:
        User: wdadaptivepy User

    """

    def __init__(self, xml_api: XMLApi) -> None:
        """Initialize UserService.

        Args:
            xml_api: wdadaptivepy XMLApi

        """
        self.__xml_api = xml_api
        self.User = User

    def get_all(
        self,
        *,
        groups: bool = True,
        owned_levels: bool = True,
    ) -> MetadataList[User]:
        """Retrieve all Users from Adaptive.

        Args:
            groups: Adaptive Groups
            owned_levels: Adaptive Owned Levels

        Returns:
            adaptive Users

        """
        include = ET.Element(
            "include",
            attrib={
                "groups": str(bool_to_str_true_false(groups)),
                "ownedLevels": str(bool_to_str_true_false(owned_levels)),
            },
        )

        response = self.__xml_api.make_xml_request(
            method="exportUsers",
            payload=include,
        )
        return MetadataList[User](User.from_xml(xml=response))

    def preview_update(
        self,
        users: Sequence[User],
        *,
        hide_password: bool = True,
    ) -> ET.Element:
        """Generate User update XML API call for review.

        Args:
            users: wdadaptivepy Users to update
            hide_password: Prevent password from being displayed

        Returns:
            XML API body

        """
        updated_users = User.to_xml("update", users)
        return self.__xml_api.preview_xml_request(
            method="importUsers",
            payload=updated_users,
            hide_password=hide_password,
        )

    def from_json(self, data: str) -> MetadataList[User]:
        """Convert JSON to MetadataList of Users.

        Args:
            data: JSON string

        Returns:
            MetadataList of Users

        """
        return MetadataList[User](User.from_json(data=data))

    def from_dict(self, data: Sequence[dict] | dict) -> MetadataList[User]:
        """Convert Python Dictionary to MetadataList of Users.

        Args:
            data: Python Dictionary

        Returns:
            MetadataList of Users

        """
        return MetadataList[User](User.from_dict(data=data))
