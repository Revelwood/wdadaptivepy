"""Tests for wdadaptivepy's service for Adaptive's Dimensions."""

# Code using pytest-mock
from unittest.mock import MagicMock
from xml.etree import ElementTree as ET

import pytest
from pytest_mock import MockerFixture

from wdadaptivepy.connectors.xml_api.xml_api import XMLApi
from wdadaptivepy.models import (
    Dimension,
    DimensionValue,
    MetadataList,
)
from wdadaptivepy.models.base import MetadataAttribute
from wdadaptivepy.services import DimensionValueService

tests: list[tuple[ET.Element, MetadataList[DimensionValue]]] = []
test_with_errors: list[tuple[ET.Element, MetadataList[Dimension], int, str]] = []

# Create Dimension values for tests
dv521 = DimensionValue(
    id=521,
    name="United States",
    description="USA",
    short_name="",
)
dv555 = DimensionValue(
    id=555,
    name="Alabama",
    description="1",
    short_name="",
    attributes=[
        MetadataAttribute(
            attribute_id=21,
            name="Education Type",
            value_id=196,
            value="Management",
        ),
    ],
)
dv555.set_adaptive_parent(dv521)
dv579 = DimensionValue(id=579, name="205", description="1", short_name="")
dv579.set_adaptive_parent(dv555)
dv4718 = DimensionValue(id=4718, name="35004", description="1", short_name="")
dv4718.set_adaptive_parent(dv579)
dv4719 = DimensionValue(id=4719, name="35005", description="", short_name="")
dv4719.set_adaptive_parent(dv579)
dv5073 = DimensionValue(id=5073, name="35006", description="", short_name="")
dv5073.set_adaptive_parent(dv579)
dv5074 = DimensionValue(id=5074, name="35007", description="", short_name="")
dv5074.set_adaptive_parent(dv579)

d16_values = MetadataList(
    [dv521, dv555, dv579, dv4718, dv4719, dv5073, dv5074],
)

d16 = Dimension(
    id=16,
    name="Geography",
    short_name="",
    auto_create=False,
    list_dimension=False,
    keep_sorted=False,
    use_on_levels=False,
    seq_no="14",
)

# TEST 1 ######################################################################
xml1 = ET.fromstring("""<?xml version='1.0' encoding='UTF-8'?>
<response success='true'>
  <output>
      <dimensions>
           <dimension id="16" name="Geography" shortName="" autoCreate="0" listDimension="0" keepSorted="0" useOnLevels="0" seqNo="14" property1="Latitude" property2="Longitude">
           </dimension>
       </dimensions>
  </output>
</response>""")  # noqa: E501
tests.append((xml1, MetadataList([])))

# TEST 2 ######################################################################
xml2 = ET.fromstring("""<?xml version='1.0' encoding='UTF-8'?>
<response success="true">
   <output>
       <dimensions>
           <dimension id="16" name="Geography" shortName="" autoCreate="0" listDimension="0" keepSorted="0" useOnLevels="0" seqNo="14" property1="Latitude" property2="Longitude">
               <dimensionValue id="521" name="United States" description="USA" shortName="">
                   <dimensionValue id="555" name="Alabama" description="1" shortName="">
                       <attributes>
                           <attribute attributeId="21" name="Education Type" valueId="196" value="Management" />
                       </attributes>
                       <dimensionValue id="579" name="205" description="1" shortName="">
                           <dimensionValue id="4718" name="35004" description="1" shortName="">
                               <properties>
                                   <property name="Latitude" value="33.606" />
                                   <property name="Longitude" value="-86.502" />
                               </properties>
                           </dimensionValue>
                           <dimensionValue id="4719" name="35005" description="" shortName="">
                               <properties>
                                   <property name="Latitude" value="33.593" />
                                   <property name="Longitude" value="-86.96" />
                               </properties>
                           </dimensionValue>
                           <dimensionValue id="5073" name="35006" description="" shortName="" />
                           <dimensionValue id="5074" name="35007" description="" shortName="" />
                       </dimensionValue>
                   </dimensionValue>
                   <properties>
                       <property name="Latitude" value="37.0902" />
                       <property name="Longitude" value="95.7129" />
                   </properties>
               </dimensionValue>
           </dimension>
       </dimensions>
   </output>
</response>""")  # noqa: E501

tests.append(
    (
        xml2,
        d16_values,
    ),
)


# From here down, we're using the original testing methodology
@pytest.fixture
def dimension_value_service() -> DimensionValueService:
    """Fixture for wdadaptivepy's Dimension Service.

    Returns:
        wdadaptivepy DimensionValueService

    """
    xml_api_instance = XMLApi("", "")
    return DimensionValueService(xml_api=xml_api_instance)


@pytest.fixture
def mock_dimension_values(
    mocker: MockerFixture,
    dimension_value_service: DimensionValueService,
) -> ET.Element:
    """Mock Adaptive's response from exportDimensions XML API.

    Args:
        mocker: pytest's mocker
        dimension_value_service: wdadaptivepy DimensionValueService to mock

    Returns:
        XML Element

    """
    # Create a mock object for the Dimensions
    mocked_levels = mocker.MagicMock()
    mocker.patch.object(
        dimension_value_service._DimensionValueService__xml_api,  # noqa: SLF001  # pyright: ignore[reportAttributeAccessIssue]
        "make_xml_request",
        mocked_levels,
    )
    return mocked_levels


@pytest.mark.parametrize(("element", "expected"), tests)
def test_get_all(
    element: ET.Element,
    expected: MetadataList[Dimension],
    dimension_value_service: DimensionValueService,
    mock_dimension_values: MagicMock,
) -> None:
    """Tests that wdadaptivepy properly parses Adaptive's exportDimensions XML API response.

    Args:
        element: Adaptive's exportDimensions XML API response
        expected: wdadaptivepy MetadataList of Dimensions
        dimension_value_service: wdadaptivepy DimensionValueService
        mock_dimension_values: Mocker for Adaptive's exportDimensions XML API response

    """  # noqa: E501
    # Set the mock object to return a specific response
    mock_dimension_values.return_value = element

    # Call the function that downloads data from the external service
    levels = dimension_value_service.get_all(d16)

    # Verify that the function returns the expected data
    assert levels == expected


@pytest.mark.parametrize(
    ("element", "expected", "index_with_error", "key_with_error"),
    test_with_errors,
)
def test_get_all_with_errors(  # noqa: PLR0913
    element: ET.Element,
    expected: MetadataList[Dimension],
    index_with_error: int,
    key_with_error: str,
    dimension_value_service: DimensionValueService,
    mock_dimension_values: MagicMock,
) -> None:
    """Tests that wdadaptivepy properly parses Adaptive's exportDimensions XML API response.

    Args:
        element: Adaptive's exportDimensions XML API response
        expected: wdadaptivepy MetadataList of Dimensions
        index_with_error: the item in the MetadataList that shouldn't match
        key_with_error: the key for the property in that item that should't match
        dimension_value_service: wdadaptivepy DimensionValueService
        mock_dimension_values: Mocker for Adaptive's exportDimensions XML API response

    """  # noqa: E501
    # Set the mock object to return a specific response
    mock_dimension_values.return_value = element

    # Call the function that downloads data from the external service
    levels = dimension_value_service.get_all(d16)

    # Verify that the function returns the expected data
    xml_value = getattr(levels[index_with_error], key_with_error, None)
    expected_value = getattr(expected[index_with_error], key_with_error, None)
    assert xml_value != expected_value
