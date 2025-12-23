"""wdadaptivepy service for Adaptive's Attributes."""

from collections.abc import Sequence
from xml.etree import ElementTree as ET

from wdadaptivepy.connectors.xml_api.xml_api import XMLApi
from wdadaptivepy.models.attribute import Attribute
from wdadaptivepy.models.base import bool_to_str_true_false
from wdadaptivepy.models.dimension import Dimension
from wdadaptivepy.models.list import MetadataList


class AttributeService:
    """Create, retrieve, and modify Adaptive Attributes.

    Attributes:
        Attribute: wdadaptivepy Attribute

    """

    def __init__(self, xml_api: XMLApi) -> None:
        """Initialize Attribute Service.

        Args:
            xml_api: wdadaptivepy XMLApi

        """
        self.__xml_api = xml_api
        self.Attribute = Attribute

    def get_all(self, *, display_name_enabled: bool = True) -> MetadataList[Attribute]:
        """Retreive all Attributes from Adaptive.

        Args:
            display_name_enabled: Include Display Name

        Returns:
            wdadaptivepy Attributes

        """
        include = ET.Element(
            "include",
            attrib={
                "displayNameEnabled": str(bool_to_str_true_false(display_name_enabled)),
            },
        )

        response = self.__xml_api.make_xml_request(
            method="exportAttributes",
            payload=include,
        )
        return MetadataList[Attribute](Attribute.from_xml(xml=response))

    def preview_update(
        self,
        attributes: Sequence[Attribute],
        *,
        hide_password: bool = True,
    ) -> ET.Element:
        """Generate Attribute update XML API call for review.

        Args:
            attributes: wdadaptivepy Attributes to update
            hide_password: Prevent password from being displayed

        Returns:
            XML API body

        """
        updated_attributes = Attribute.to_xml("update", attributes)
        return self.__xml_api.preview_xml_request(
            method="importAttributes",
            payload=updated_attributes,
            hide_password=hide_password,
        )

    def get(  # NOQA: PLR0912 PLR0913 C901
        self,
        attributes: Sequence[Attribute] = [],
        attribute_ids: Sequence[int] = [],
        attribute_names: Sequence[str] = [],
        attribute_types: Sequence[str] = [],
        dimensions: Sequence[Dimension] = [],
        dimension_ids: Sequence[int] = [],
        *,
        display_name_enabled: bool = True,
    ) -> MetadataList[Attribute]:
        """Retrieve Attributes from Adaptive based on parameters.

        Args:
            attributes: wdadaptivepy Attributes
            attribute_ids: ID of Attributes
            attribute_names: Name of Attributes
            attribute_types: Type of Attribute (eg: Level, Account, Dimension)
            dimensions: wdadaptivepy Dimensions
            dimension_ids: ID of Dimensions
            display_name_enabled: Include Display Name for each Attribute

        Returns:
            wdadaptivepy Attributes

        """
        ids: list[int] = []
        if attributes:
            ids.extend(
                [attribute.id for attribute in attributes if attribute.id is not None],
            )
        elif attribute_ids:
            ids.extend(attribute_ids)
        elif attribute_names:
            all_attributes = self.get_all()
            for name in attribute_names:
                for attribute in all_attributes:
                    if name == attribute.name and attribute.id is not None:
                        ids.append(attribute.id)
                        break
        elif attribute_types:
            all_attributes = self.get_all()
            for attribute_type in attribute_types:
                for attribute in all_attributes:
                    if (
                        attribute_type == attribute.attribute_type
                        and attribute.id is not None
                    ):
                        ids.append(attribute.id)
                        break
        elif not (dimensions or dimension_ids):
            all_attributes = self.get_all()
            if dimensions:
                for dimension in dimensions:
                    for attribute in all_attributes:
                        if (
                            attribute.dimension_id == dimension.id
                            and attribute.id is not None
                        ):
                            ids.append(attribute.id)
                            break
            elif dimension_ids:
                for dimension_id in dimension_ids:
                    for attribute in all_attributes:
                        if (
                            attribute.dimension_id == dimension_id
                            and attribute.id is not None
                        ):
                            ids.append(attribute.id)
                            break
        else:
            raise ValueError
        if not ids:
            raise ValueError

        include = ET.Element(
            "include",
            attrib={
                "attributeIDs": ",".join(str(attribute_id) for attribute_id in ids),
                "displayNameEnabled": str(bool_to_str_true_false(display_name_enabled)),
            },
        )

        response = self.__xml_api.make_xml_request(
            method="exportAttributes",
            payload=include,
        )
        return MetadataList[Attribute](Attribute.from_xml(xml=response))

    def from_json(self, data: str) -> MetadataList[Attribute]:
        """Convert JSON to MetadataList of Attributes.

        Args:
            data: JSON data

        Returns:
            MetadataList of Attributes

        """
        return MetadataList[Attribute](Attribute.from_json(data=data))

    def from_dict(self, data: Sequence[dict] | dict) -> MetadataList[Attribute]:
        """Convert Python Dictionary to MetadataList of Attributes.

        Args:
            data: Python Dictionary

        Returns:
            MetadataList of Attributes

        """
        return MetadataList[Attribute](Attribute.from_dict(data=data))
