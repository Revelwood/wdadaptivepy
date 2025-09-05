"""Tests for wdadaptivepy's service for Adaptive's Levels."""

# Code using pytest-mock
from unittest.mock import MagicMock
from xml.etree import ElementTree as ET

import pytest
from pytest_mock import MockerFixture

from wdadaptivepy.connectors.xml_api.xml_api import XMLApi
from wdadaptivepy.models import Level, MetadataAttribute, MetadataList
from wdadaptivepy.services import LevelService

tests: list[tuple[ET.Element, MetadataList[Level]]] = []

# TEST 1 ######################################################################
xml1 = ET.fromstring("""<?xml version='1.0' encoding='UTF-8'?>
<response success='true'>
  <output>
    <levels seqNo='0' displayNameType='NAME'>
      <level id='123'/>
    </levels>
  </output>
</response>""")
tests.append((xml1, MetadataList([Level(id=123)])))

# TEST 2 ######################################################################
xml2 = ET.fromstring("""<?xml version='1.0' encoding='UTF-8'?>
<response success='true'>
  <output>
    <levels seqNo='0' displayNameType='NAME'>
      <level id='124' name='hello'/>
    </levels>
  </output>
</response>""")
tests.append((xml2, MetadataList([Level(id=124, name="hello")])))

# TEST 3 ######################################################################
xml3 = ET.fromstring("""<?xml version='1.0' encoding='UTF-8'?>
<response success='true'>
  <output>
    <levels seqNo='0' displayNameType='NAME'>
      <level id='125' name='Revelwood'/>
    </levels>
  </output>
</response>""")
tests.append((xml3, MetadataList([Level(id=125, name="Revelwood")])))

# TEST 4 ######################################################################
xml4 = ET.fromstring("""<?xml version='1.0' encoding='UTF-8'?>
<response success='true'>
  <output>
  </output>
</response>""")
tests.append((xml4, MetadataList([])))

# TEST 5 ######################################################################
xml5 = ET.fromstring("""<?xml version="1.0" encoding="UTF-8"?>
<response success="true">
  <output>
    <levels seqNo="0" displayNameType="NAME">
      <level id="1" code="Total Company" name="Total Company">
        <level id="201" code="BC - 52" name="Company A (100% owned)">
          <level id="164" code="BC - 70" name="Operations - company A">
            <level id="165" code="BC - 111" name="United States">
              <level id="166" code="BC - 91" name="Sales - North" />
              <level id="167" code="BC - 93" name="Sales - South" />
              <level id="168" code="BC - 86" name="Sales - East">
                     <attributes>
                        <attribute attributeId="1" name="color" value="blue" valueId="20"/>
                        <attribute attributeId="2" name="size" value="medium" valueId="21"/>
                     </attributes>
              </level>
              <level id="169" code="BC - 98" name="Sales - West"/>
              <level id="170" code="BC - 101" name="Services - East" />
              <level id="171" code="BC - 104" name="Services - West" />
              <level id="172" code="BC - 105" name="Support" />
            </level>
          </level>
        </level>
      </level>
    </levels>
  </output>
</response>""")  # noqa: E501

# Create Levels
l1 = Level(id=1, code="Total Company", name="Total Company")
l201 = Level(id=201, code="BC - 52", name="Company A (100% owned)")
l164 = Level(id=164, code="BC - 70", name="Operations - company A")
l165 = Level(id=165, code="BC - 111", name="United States")
l166 = Level(id=166, code="BC - 91", name="Sales - North")
l167 = Level(id=167, code="BC - 93", name="Sales - South")
l168 = Level(id=168, code="BC - 86", name="Sales - East")
av1 = MetadataAttribute(attribute_id=1, name="color", value="blue", value_id=20)
l168.set_adaptive_attribute(av1)
av2 = MetadataAttribute(attribute_id=2, name="size", value="medium", value_id=21)
l168.set_adaptive_attribute(av2)
l169 = Level(id=169, code="BC - 98", name="Sales - West")
l170 = Level(id=170, code="BC - 101", name="Services - East")
l171 = Level(id=171, code="BC - 104", name="Services - West")
l172 = Level(id=172, code="BC - 105", name="Support")

# Set up hierarchy
l201.set_adaptive_parent(l1)
l164.set_adaptive_parent(l201)
l165.set_adaptive_parent(l164)
l166.set_adaptive_parent(l165)
l167.set_adaptive_parent(l165)
l168.set_adaptive_parent(l165)
l169.set_adaptive_parent(l165)
l170.set_adaptive_parent(l165)
l171.set_adaptive_parent(l165)
l172.set_adaptive_parent(l165)

tests.append(
    (
        xml5,
        MetadataList([l1, l201, l164, l165, l166, l167, l168, l169, l170, l171, l172]),
    ),
)

# TEST 6 ######################################################################
xml6 = ET.fromstring("""<?xml version="1.0" encoding="UTF-8"?>
<response success="true">
  <output>
    <levels seqNo="0" displayNameType="NAME">
      <level id="1" code="Total Company" name="Total Company">
        <level id="201" code="BC - 52" name="Company A (100% owned)">
          <level id="164" code="BC - 70" name="Operations - company A">
            <level id="165" code="BC - 111" name="United States">
              <level id="166" code="BC - 91" name="Sales - North" />
              <level id="167" code="BC - 93" name="Sales - South" />
              <level id="168" code="BC - 86" name="Sales - East">
                <attributes>
                  <attribute attributeId="1" name="color" value="blue" valueId="20"/>
                </attributes>
                <level id="169" code="BC - 98" name="Sales - West"/>
              </level>
              <level id="170" code="BC - 101" name="Services - East" />
              <level id="171" code="BC - 104" name="Services - West" />
              <level id="172" code="BC - 105" name="Support" />
            </level>
          </level>
        </level>
      </level>
    </levels>
  </output>
</response>""")


test_with_errors: list[tuple[ET.Element, MetadataList[Level], int, str]] = []
test_with_errors.append(
    (
        xml6,
        MetadataList([l1, l201, l164, l165, l166, l167, l168, l169, l170, l171, l172]),
        7,
        "adaptive_parent",
    ),
)


# From here down, we're using the original testing methodology
@pytest.fixture
def level_service() -> LevelService:
    """Fixture for wdadaptivepy's Level Service.

    Returns:
        wdadaptivepy LevelService

    """
    xml_api_instance = XMLApi("", "")
    return LevelService(xml_api=xml_api_instance)


@pytest.fixture
def mock_levels(mocker: MockerFixture, level_service: LevelService) -> ET.Element:
    """Mock Adaptive's response from exportLevels XML API.

    Args:
        mocker: pytest's mocker
        level_service: wdadaptivepy LevelService to mock

    Returns:
        XML Element

    """
    # Create a mock object for the Levels
    mocked_levels = mocker.MagicMock()
    mocker.patch.object(
        level_service._LevelService__xml_api,  # noqa: SLF001  # pyright: ignore[reportAttributeAccessIssue]
        "make_xml_request",
        mocked_levels,
    )
    return mocked_levels


@pytest.mark.parametrize(("element", "expected"), tests)
def test_get_all(
    element: ET.Element,
    expected: MetadataList[Level],
    level_service: LevelService,
    mock_levels: MagicMock,
) -> None:
    """Tests that wdadaptivepy properly parses Adaptive's exportLevels XML API response.

    Args:
        element: Adaptive's exportLevels XML API response
        expected: wdadaptivepy MetadataList of Levels
        level_service: wdadaptivepy LevelService
        mock_levels: Mocker for Adaptive's exportLevels XML API response

    """
    # Set the mock object to return a specific response
    mock_levels.return_value = element

    # Call the function that downloads data from the external service
    levels = level_service.get_all()

    # Verify that the function returns the expected data
    assert levels == expected


@pytest.mark.parametrize(
    ("element", "expected", "index_with_error", "key_with_error"),
    test_with_errors,
)
def test_get_all_with_errors(  # noqa: PLR0913
    element: ET.Element,
    expected: MetadataList[Level],
    index_with_error: int,
    key_with_error: str,
    level_service: LevelService,
    mock_levels: MagicMock,
) -> None:
    """Tests that wdadaptivepy properly parses Adaptive's exportLevels XML API response.

    Args:
        element: Adaptive's exportLevels XML API response
        expected: wdadaptivepy MetadataList of Levels
        index_with_error: the item in the MetadataList that shouldn't match
        key_with_error: the key for the property in that item that should't match
        level_service: wdadaptivepy LevelService
        mock_levels: Mocker for Adaptive's exportLevels XML API response

    """
    # Set the mock object to return a specific response
    mock_levels.return_value = element

    # Call the function that downloads data from the external service
    levels = level_service.get_all()

    # Verify that the function returns the expected data
    xml_value = getattr(levels[index_with_error], key_with_error, None)
    expected_value = getattr(expected[index_with_error], key_with_error, None)
    assert xml_value != expected_value
