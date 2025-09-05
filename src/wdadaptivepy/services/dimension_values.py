"""wdadaptivepy service for Adaptive's Dimension Values."""

from collections.abc import Sequence
from xml.etree import ElementTree as ET

from wdadaptivepy.connectors.xml_api.xml_api import XMLApi
from wdadaptivepy.models.base import bool_to_str_true_false
from wdadaptivepy.models.dimension import Dimension
from wdadaptivepy.models.dimension_value import DimensionValue
from wdadaptivepy.models.list import MetadataList


class DimensionValueService:
    """Create, retrieve, and modify Adaptive Dimensions.

    Attributes:
        Dimension: wdadaptivepy Dimension

    """

    def __init__(self, xml_api: XMLApi) -> None:
        """Initialize DimensionService.

        Args:
            xml_api: wdadaptivepy XMLApi

        """
        self.__xml_api = xml_api
        self.DimensionValue = DimensionValue

    def get_all(
        self,
        dimension: Dimension | str | int,
        *,
        attributes: bool = True,
        display_name_enabled: bool = True,
    ) -> MetadataList[DimensionValue]:
        """Retrieve all Dimension Values from Adaptive.

        Args:
            dimension: Adaptive Dimension
            attributes: Adaptive Attributes
            display_name_enabled: Adaptive Display Name Enabled

        Returns:
            adaptive Dimension Values

        """
        get_dimension = self.__find_dimension(dimension)
        include = ET.Element(
            "include",
            attrib={
                "dimensionIDs": str(get_dimension.id),
                "attributes": str(bool_to_str_true_false(attributes)),
                "displayNameEnabled": str(bool_to_str_true_false(display_name_enabled)),
            },
        )

        response = self.__xml_api.make_xml_request(
            method="exportDimensions",
            payload=include,
        )
        return MetadataList[DimensionValue](DimensionValue.from_xml(xml=response))

    def preview_update(
        self,
        dimension: Dimension | str | int,
        dimension_values: Sequence[DimensionValue],
        *,
        hide_password: bool = True,
    ) -> ET.Element:
        """Generate Dimension Value update XML API call for review.

        Args:
            dimension: wdadaptivepy Dimension to update
            dimension_values: wdadaptivepy Dimension Values to update
            hide_password: Prevent password from being displayed

        Returns:
            XML API body

        """
        method, payload = self.__build_update_payload(dimension, dimension_values)
        # ET.indent(updated_dimensions)
        # with open("test_dimensions.xml", "w", encoding="utf-8") as fp:
        #     fp.write(ET.tostring(update_dimension, encoding="unicode"))
        return self.__xml_api.preview_xml_request(
            method=method,
            payload=payload,
            hide_password=hide_password,
        )

    def __build_update_payload(
        self,
        dimension: Dimension | int | str,
        dimension_values: Sequence[DimensionValue],
    ) -> tuple[str, ET.Element]:
        for dimension_value in dimension_values:
            if dimension_value.id is None or dimension_value.id == 0:
                raise ValueError
        found_dimension = self.__find_dimension(dimension)
        update_dimensions = Dimension.to_xml(
            "update",
            [Dimension(id=found_dimension.id)],
        )
        update_dimension = update_dimensions.find("dimension")
        if update_dimension is None:
            raise ValueError
        update_dimension.extend(DimensionValue.to_xml("update", dimension_values))
        return "updateDimensions", update_dimensions

    def __find_dimension(self, dimension: Dimension | int | str) -> Dimension:  # NOQA: PLR0912
        search_dimension = None
        if isinstance(dimension, Dimension):
            search_dimension = dimension
        elif isinstance(dimension, int):
            search_dimension = Dimension(id=dimension)
        elif isinstance(dimension, str):
            search_dimension = Dimension(code=dimension, name=dimension)
        else:
            raise TypeError

        dimensions_include = ET.Element(
            "include",
            attrib={
                "attributes": str(bool_to_str_true_false(value=False)),
                "dimensionValues": str(bool_to_str_true_false(value=False)),
                "displayNameEnabled": str(bool_to_str_true_false(value=True)),
            },
        )
        dimensions_response = self.__xml_api.make_xml_request(
            method="exportDimensions",
            payload=dimensions_include,
        )
        all_dimensions = MetadataList[Dimension](
            Dimension.from_xml(xml=dimensions_response),
        )

        found_dimension = None
        if search_dimension.id is not None and search_dimension.id != 0:
            for dim in all_dimensions:
                if dim.id == search_dimension.id:
                    found_dimension = dim
                    break
        else:
            for dim in all_dimensions:
                if dim.code == search_dimension.code:
                    found_dimension = dim
                    break
            if search_dimension is None:
                for dim in all_dimensions:
                    if dim.name == search_dimension.name:
                        found_dimension = dim
                        break

        if found_dimension is None:
            raise ValueError

        return found_dimension

    def from_json(self, data: str) -> MetadataList[DimensionValue]:
        """Convert JSON to MetadataList of Dimension Values.

        Args:
            data: JSON string

        Returns:
            MetadataList of Dimension Values

        """
        return MetadataList[DimensionValue](DimensionValue.from_json(data=data))

    def from_dict(self, data: Sequence[dict] | dict) -> MetadataList[DimensionValue]:
        """Convert Python Dictionary to MetadataList of Dimension Values.

        Args:
            data: Python Dictionary

        Returns:
            MetadataList of Dimension Values

        """
        return MetadataList[DimensionValue](DimensionValue.from_dict(data=data))
