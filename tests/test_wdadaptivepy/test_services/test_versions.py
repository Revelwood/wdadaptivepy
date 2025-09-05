"""Tests for wdadaptivepy's service for Adaptive's Versions."""

# Code using pytest-mock
from unittest.mock import MagicMock
from xml.etree import ElementTree as ET

import pytest
from pytest_mock import MockerFixture

from wdadaptivepy.connectors.xml_api.xml_api import XMLApi
from wdadaptivepy.models import (
    MetadataList,
    Version,
)
from wdadaptivepy.services import VersionService

tests: list[tuple[ET.Element, MetadataList[Version]]] = []
test_with_errors: list[tuple[ET.Element, MetadataList[Version], int, str]] = []

# Create Versions

v1 = Version(
    id=1,
    name="Actuals",
    short_name="",
    version_type="ACTUALS",
    is_virtual=False,
    description="Total Actuals",
    is_default_version=False,
    is_locked=False,
    has_audit_trail=False,
    is_importable=False,
    start_ver="2012",
    completed_values_thru="03/2012",
    start_scroll="01/2012",
    end_ver="2016",
    lock_leading="",
)
v5 = Version(
    id=5,
    name="Adjusted Actuals",
    short_name="SV-13",
    version_type="ACTUALS",
    is_virtual=False,
    description="Actuals SubVersion",
    is_default_version=False,
    is_locked=False,
    has_audit_trail=False,
    is_importable=False,
    parent=v1,
)
v6 = Version(
    id=6,
    name="Original Import",
    short_name="SSV-13",
    version_type="ACTUALS",
    is_virtual=False,
    description="Values Imported from the GL",
    is_default_version=False,
    is_locked=False,
    has_audit_trail=False,
    is_importable=True,
    parent=v5,
)
v8 = Version(
    id=8,
    name="Manual Adjustments",
    short_name="SSV-14",
    version_type="ACTUALS",
    is_virtual=False,
    description="Actuals Sub-Version for Manual Adjustments",
    is_default_version=False,
    is_locked=False,
    has_audit_trail=True,
    is_importable=True,
    parent=v5,
)
v9 = Version(
    id=9,
    name="Eliminations",
    short_name="ELIM",
    version_type="ACTUALS",
    is_virtual=False,
    description="Eliminating entries",
    is_default_version=False,
    is_locked=False,
    has_audit_trail=False,
    is_importable=False,
    parent=v1,
)
v2 = Version(
    id=2,
    name="Budget 2013",
    short_name="",
    version_type="PLANNING",
    is_virtual=False,
    description="This is the budget for 2013 with a five-year span.",
    is_default_version=True,
    is_locked=False,
    has_audit_trail=True,
    is_importable=True,
    left_scroll="2013",
    start_plan="01/2013",
    end_plan="2017",
    lock_leading="05/2013",
)
v10 = Version(
    id=10,
    name="Worst Case",
    short_name="S13-A-WC",
    version_type="SCENARIO",
    is_virtual=False,
    description="Worst Case for Budget 2013",
    is_default_version=False,
    is_locked=False,
    has_audit_trail=False,
    is_importable=False,
    is_predictive=False,
    parent=v2,
)
v3 = Version(
    id=3,
    name="Budget 2014",
    short_name="B-14",
    version_type="PLANNING",
    is_virtual=False,
    description="This is the budget for 2014 with a five-year span.",
    is_default_version=False,
    is_locked=False,
    has_audit_trail=False,
    is_importable=True,
    left_scroll="2014",
    start_plan="01/2014",
    end_plan="2018",
    lock_leading="",
)

# TEST 1 ######################################################################
xml1 = ET.fromstring("""<?xml version='1.0' encoding='UTF-8'?>
<response success='true'>
  <output>
  </output>
</response>""")
tests.append((xml1, MetadataList([])))

# TEST 2 ######################################################################
xml2 = ET.fromstring("""<?xml version='1.0' encoding='UTF-8'?>
<response success="true">
<output>
<versions seqNo="32">
  <version id="1" name="Actuals" shortName="" type="ACTUALS" isVirtual="false" description="Total Actuals" isDefaultVersion="false"
           isLocked="false" hasAuditTrail="false" isImportable="0"
           startVer="2012" completedValuesThru="03/2012"
           startScroll="01/2012" endVer="2016" lockLeading="" >
    <version id="5" name="Adjusted Actuals" shortName="SV-13" type="ACTUALS" isVirtual="false" description="Actuals SubVersion" isDefaultVersion="false"
             isLocked="false" hasAuditTrail="false" isImportable="0" >
      <version id="6" name="Original Import" shortName="SSV-13" type="ACTUALS" isVirtual="false" description="Values Imported from the GL" isDefaultVersion="false"
               isLocked="false" hasAuditTrail="false" isImportable="1" />
      <version id="8" name="Manual Adjustments" shortName="SSV-14" type="ACTUALS" isVirtual="false" description="Actuals Sub-Version for Manual Adjustments" isDefaultVersion="false"
               isLocked="false" hasAuditTrail="true" isImportable="1" />
    </version>
    <version id="9" name="Eliminations" shortName="ELIM" type="ACTUALS" isVirtual="false" description="Eliminating entries" isDefaultVersion="false"
             isLocked="false" hasAuditTrail="false" isImportable="0" />
  </version>
  <version id="2" name="Budget 2013" shortName="" type="PLANNING" isVirtual="false" description="This is the budget for 2013 with a five-year span." isDefaultVersion="true"
           isLocked="false" hasAuditTrail="true" isImportable="1"
           leftScroll="2013" startPlan="01/2013" endPlan="2017" lockLeading="05/2013">
    <version id="10" name="Worst Case" shortName="S13-A-WC" type="SCENARIO" isVirtual="false" description="Worst Case for Budget 2013" isDefaultVersion="false" isLocked="false"
             hasAuditTrail="false" isImportable="0" isPredictive="false" />
  </version>
 <version id="3" name="Budget 2014" shortName="B-14" type="PLANNING" isVirtual="false" description="This is the budget for 2014 with a five-year span." isDefaultVersion="false"
           isLocked="false" hasAuditTrail="false" isImportable="1"
           leftScroll="2014" startPlan="01/2014" endPlan="2018" lockLeading="" />
</versions>
</output>
</response>""")  # noqa: E501

tests.append(
    (
        xml2,
        MetadataList([v1, v5, v6, v8, v9, v2, v10, v3]),
    ),
)


# From here down, we're using the original testing methodology
@pytest.fixture
def version_service() -> VersionService:
    """Fixture for wdadaptivepy's Version Service.

    Returns:
        wdadaptivepy VersionService

    """
    xml_api_instance = XMLApi("", "")
    return VersionService(xml_api=xml_api_instance)


@pytest.fixture
def mock_versions(
    mocker: MockerFixture,
    version_service: VersionService,
) -> ET.Element:
    """Mock Adaptive's response from exportVersions XML API.

    Args:
        mocker: pytest's mocker
        version_service: wdadaptivepy VersionService to mock

    Returns:
        XML Element

    """
    # Create a mock object for the Versions
    mocked_levels = mocker.MagicMock()
    mocker.patch.object(
        version_service._VersionService__xml_api,  # noqa: SLF001  # pyright: ignore[reportAttributeAccessIssue]
        "make_xml_request",
        mocked_levels,
    )
    return mocked_levels


@pytest.mark.parametrize(("element", "expected"), tests)
def test_get_all(
    element: ET.Element,
    expected: MetadataList[Version],
    version_service: VersionService,
    mock_versions: MagicMock,
) -> None:
    """Tests that wdadaptivepy properly parses Adaptive's exportVersions API response.

    Args:
        element: Adaptive's exportVersions XML API response
        expected: wdadaptivepy MetadataList of Versions
        version_service: wdadaptivepy VersionService
        mock_versions: Mocker for Adaptive's exportVersions XML API response

    """
    # Set the mock object to return a specific response
    mock_versions.return_value = element

    # Call the function that downloads data from the external service
    levels = version_service.get_all()

    # Verify that the function returns the expected data
    assert levels == expected


@pytest.mark.parametrize(
    ("element", "expected", "index_with_error", "key_with_error"),
    test_with_errors,
)
def test_get_all_with_errors(  # noqa: PLR0913
    element: ET.Element,
    expected: MetadataList[Version],
    index_with_error: int,
    key_with_error: str,
    version_service: VersionService,
    mock_versions: MagicMock,
) -> None:
    """Tests that wdadaptivepy properly parses Adaptive's exportVersions API response.

    Args:
        element: Adaptive's exportVersions XML API response
        expected: wdadaptivepy MetadataList of Versions
        index_with_error: the item in the MetadataList that shouldn't match
        key_with_error: the key for the property in that item that should't match
        version_service: wdadaptivepy VersionService
        mock_versions: Mocker for Adaptive's exportVersions XML API response

    """
    # Set the mock object to return a specific response
    mock_versions.return_value = element

    # Call the function that downloads data from the external service
    levels = version_service.get_all()

    # Verify that the function returns the expected data
    xml_value = getattr(levels[index_with_error], key_with_error, None)
    expected_value = getattr(expected[index_with_error], key_with_error, None)
    assert xml_value != expected_value
