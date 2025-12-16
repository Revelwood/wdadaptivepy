"""wdadaptivepy service for Adaptive's Dimensions."""

from collections.abc import Sequence
from xml.etree import ElementTree as ET

from wdadaptivepy.connectors.xml_api.xml_api import XMLApi
from wdadaptivepy.models.base import bool_to_str_true_false
from wdadaptivepy.models.dimension import Dimension
from wdadaptivepy.models.list import MetadataList


class DimensionService:
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
        self.Dimension = Dimension

    def get_all(
        self,
        *,
        attributes: bool = True,
        dimension_values: bool = True,
        display_name_enabled: bool = True,
    ) -> MetadataList[Dimension]:
        """Retrieve all Dimensions from Adaptive.

        Args:
            attributes: Adaptive Attributes
            dimension_values: Adaptive Dimension Values
            display_name_enabled: Adaptive Display Name Enabled

        Returns:
            adaptive Dimensions

        """
        include = ET.Element(
            "include",
            attrib={
                "attributes": str(bool_to_str_true_false(attributes)),
                "dimensionValues": str(bool_to_str_true_false(dimension_values)),
                "displayNameEnabled": str(bool_to_str_true_false(display_name_enabled)),
            },
        )

        response = self.__xml_api.make_xml_request(
            method="exportDimensions",
            payload=include,
        )
        return MetadataList[Dimension](Dimension.from_xml(xml=response))

    def preview_update(
        self,
        dimensions: Sequence[Dimension],
        *,
        hide_password: bool = True,
    ) -> ET.Element:
        """Generate Dimension update XML API call for review.

        Args:
            dimensions: wdadaptivepy Dimensions to update
            hide_password: Prevent password from being displayed

        Returns:
            XML API body

        """
        updated_dimensions = Dimension.to_xml("update", dimensions)
        return self.__xml_api.preview_xml_request(
            method="importDimensions",
            payload=updated_dimensions,
            hide_password=hide_password,
        )

    def get(  # NOQA: PLR0913
        self,
        dimensions: Sequence[Dimension] = [],
        dimension_ids: Sequence[int] = [],
        dimension_names: Sequence[str] = [],
        *,
        attributes: bool = True,
        dimension_values: bool = True,
        display_name_enabled: bool = True,
    ) -> MetadataList[Dimension]:
        """Retrieve Dimensions from Adaptive with additional filters.

        Args:
            dimensions: Adaptive Dimensions
            dimension_ids: Adaptive Dimension IDs
            dimension_names: Adaptive Dimension Names
            attributes: Adaptive Attributes
            dimension_values: Adaptive Dimension Values
            display_name_enabled: Adaptive Display Name Enabled

        Returns:
            adaptive Dimensions

        """
        ids: list[int] = []
        if dimensions:
            ids.extend(
                [dimension.id for dimension in dimensions if dimension.id is not None],
            )
        elif dimension_ids:
            ids.extend(dimension_ids)
        elif dimension_names:
            all_dimensions = self.get_all(dimension_values=False)
            for name in dimension_names:
                ids.extend(
                    [
                        dimension.id
                        for dimension in all_dimensions
                        if dimension.name == name and dimension.id is not None
                    ],
                )
        else:
            raise ValueError
        if not ids:
            raise ValueError

        include = ET.Element(
            "include",
            attrib={
                "dimensionIDs": ",".join(str(dimension_id) for dimension_id in ids),
                "attributes": str(bool_to_str_true_false(attributes)),
                "dimensionValues": str(bool_to_str_true_false(dimension_values)),
                "displayNameEnabled": str(bool_to_str_true_false(display_name_enabled)),
            },
        )

        response = self.__xml_api.make_xml_request(
            method="exportDimensions",
            payload=include,
        )
        return MetadataList[Dimension](Dimension.from_xml(xml=response))

    def from_json(self, data: str) -> MetadataList[Dimension]:
        """Convert JSON to MetadataList of Dimensions.

        Args:
            data: JSON string

        Returns:
            MetadataList of Dimensions

        """
        return MetadataList[Dimension](Dimension.from_json(data=data))

    def from_dict(self, data: Sequence[dict] | dict) -> MetadataList[Dimension]:
        """Convert Python Dictionary to MetadataList of Dimensions.

        Args:
            data: Python Dictionary

        Returns:
            MetadataList of Dimensions

        """
        return MetadataList[Dimension](Dimension.from_dict(data=data))
