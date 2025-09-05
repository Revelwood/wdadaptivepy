"""wdadaptivepy service for Adaptive's Attribute Values."""

from collections.abc import Sequence
from xml.etree import ElementTree as ET

from wdadaptivepy.connectors.xml_api.xml_api import XMLApi
from wdadaptivepy.models.attribute import Attribute
from wdadaptivepy.models.attribute_value import AttributeValue
from wdadaptivepy.models.base import bool_to_str_true_false
from wdadaptivepy.models.list import MetadataList


class AttributeValueService:
    """Create, retrieve, and modify Adaptive Attribute Values.

    Attributes:
        AttributeValue: wdadaptivepy AttributeValue

    """

    def __init__(self, xml_api: XMLApi) -> None:
        """Initialize Attribute Service.

        Args:
            xml_api: wdadaptivepy XMLApi

        """
        self.__xml_api = xml_api
        self.AttributeValue = AttributeValue

    def get_all(
        self,
        attribute: Attribute | str | int,
        *,
        display_name_enabled: bool = True,
    ) -> MetadataList[AttributeValue]:
        """Retreive all Attribute Values from Adaptive.

        Args:
            attribute: Adaptive Attribute
            display_name_enabled: Include Display Name

        Returns:
            wdadaptivepy Attribute Values

        """
        _, attribute_values = self.__find_attribute(
            attribute,
            display_name_enabled=display_name_enabled,
        )
        return attribute_values

    def preview_update(
        self,
        attribute: Attribute | int | str,
        attribute_values: Sequence[AttributeValue],
        *,
        hide_password: bool = True,
    ) -> ET.Element:
        """Generate Attribute update XML API call for review.

        Args:
            attribute: adaptivepy Attribute
            attribute_values: wdadaptivepy Attribute Values to update
            hide_password: Prevent password from being displayed

        Returns:
            XML API body

        """
        method, payload = self.__build_update_payload(attribute, attribute_values)
        # updated_attributes = Attribute.to_xml("update", attributes)
        # ET.indent(updated_attributes)
        # with open("test_attributes.xml", "w", encoding="utf-8") as fp:
        #     fp.write(ET.tostring(updated_attributes, encoding="unicode"))
        return self.__xml_api.preview_xml_request(
            method=method,
            payload=payload,
            hide_password=hide_password,
        )

    def __build_update_payload(
        self,
        attribute: Attribute | int | str,
        attribute_values: Sequence[AttributeValue],
    ) -> tuple[str, ET.Element]:
        for attribute_value in attribute_values:
            if attribute_value.id is None or attribute_value.id == 0:
                raise ValueError
        found_attribute, _ = self.__find_attribute(attribute=attribute)
        update_attributes = Attribute.to_xml(
            "update",
            [Attribute(id=found_attribute.id)],
        )
        update_attribute = update_attributes.find("attribute")
        if update_attribute is None:
            raise ValueError
        update_attribute.extend(
            AttributeValue.to_xml("update", attribute_values),
        )
        return "updateAttributes", update_attributes

    def __find_attribute(
        self,
        attribute: Attribute | int | str,
        *,
        display_name_enabled: bool = True,
    ) -> tuple[Attribute, MetadataList[AttributeValue]]:
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

        attributes = MetadataList[Attribute](Attribute.from_xml(xml=response))
        attribute_check = Attribute()
        if isinstance(attribute, Attribute):
            attribute_check = attribute
        elif isinstance(attribute, int):
            attribute_check.id = attribute
        elif isinstance(attribute, str):
            attribute_check.name = attribute
        else:
            raise TypeError

        found_attribute = None
        for attr in attributes:
            if attr.id == attribute_check.id or attr.name == attribute_check.name:
                found_attribute = attr
                break
        if found_attribute is None:
            raise ValueError

        found_xml_elem = None
        for elem in response.iter("attribute"):
            if elem.get("id") == str(found_attribute.id):
                found_xml_elem = elem
                break
        if found_xml_elem is None:
            raise ValueError
        found_attribute_values = AttributeValue.from_xml(found_xml_elem)

        return found_attribute, found_attribute_values

    def from_json(self, data: str) -> MetadataList[AttributeValue]:
        """Convert JSON to MetadataList of Attribute Values.

        Args:
            data: JSON data

        Returns:
            MetadataList of Attribute Values

        """
        return MetadataList[AttributeValue](AttributeValue.from_json(data=data))

    def from_dict(self, data: Sequence[dict] | dict) -> MetadataList[AttributeValue]:
        """Convert Python Dictionary to MetadataList of Attribute Values.

        Args:
            data: Python Dictionary

        Returns:
            MetadataList of Attribute Value

        """
        return MetadataList[AttributeValue](AttributeValue.from_dict(data=data))
