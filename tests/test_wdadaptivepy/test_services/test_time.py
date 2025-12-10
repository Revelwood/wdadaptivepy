"""Tests for wdadaptivepy's service for Adaptive's Times."""

# Code using pytest-mock
from datetime import datetime
from unittest.mock import MagicMock
from xml.etree import ElementTree as ET

import pytest
from pytest_mock import MockerFixture

from wdadaptivepy.connectors.xml_api.xml_api import XMLApi
from wdadaptivepy.models import (
    MetadataList,
    Time,
)
from wdadaptivepy.models.time import Period, Stratum
from wdadaptivepy.services import TimeService

tests: list[tuple[ET.Element, MetadataList[Time]]] = []
test_with_errors: list[tuple[ET.Element, MetadataList[Time], int, str]] = []

# Create Times for tests
s3 = Stratum(code="year", label="Year", short_name="Yr", id=3, in_use=True)
s2 = Stratum(
    code="qtr",
    label="Quarter",
    short_name="Qtr",
    id=2,
    in_use=True,
    parent=s3,
)
s1 = Stratum(
    code="month",
    label="Month",
    short_name="Mon",
    id=1,
    in_use=True,
    is_default=True,
    parent=s2,
)

p2015 = Period(
    code="2015",
    label="FY2015",
    short_name="FY2015",
    stratum_id=3,
    id=15003,
    end=datetime(2016, 1, 1),  # NOQA: DTZ001
)

p2015_q1 = Period(
    code="Q1-2015",
    label="Q1-FY15",
    short_name="Q1-FY15",
    stratum_id=2,
    id=60002,
    end=datetime(2015, 4, 1),  # NOQA: DTZ001
    parent=p2015,
)
p2015_jan = Period(
    code="01/2015",
    label="Jan-2015",
    short_name="Jan-2015",
    stratum_id=1,
    id=180001,
    end=datetime(2015, 2, 1),  # NOQA: DTZ001
    parent=p2015_q1,
)
p2015_feb = Period(
    code="02/2015",
    label="Feb-2015",
    short_name="Feb-2015",
    stratum_id=1,
    id=181001,
    end=datetime(2015, 3, 1),  # NOQA: DTZ001
    parent=p2015_q1,
)
p2015_mar = Period(
    code="03/2015",
    label="Mar-2015",
    short_name="Mar-2015",
    stratum_id=1,
    id=182001,
    end=datetime(2015, 4, 1),  # NOQA: DTZ001
    parent=p2015_q1,
)
p2015_q2 = Period(
    code="Q2-2015",
    label="Q2-FY15",
    short_name="Q2-FY15",
    stratum_id=2,
    id=61002,
    end=datetime(2015, 7, 1),  # NOQA: DTZ001
    parent=p2015,
)
p2015_apr = Period(
    code="04/2015",
    label="Apr-2015",
    short_name="Apr-2015",
    stratum_id=1,
    id=183001,
    end=datetime(2015, 5, 1),  # NOQA: DTZ001
    parent=p2015_q2,
)
p2015_may = Period(
    code="05/2015",
    label="May-2015",
    short_name="May-2015",
    stratum_id=1,
    id=184001,
    end=datetime(2015, 6, 1),  # NOQA: DTZ001
    parent=p2015_q2,
)
p2015_jun = Period(
    code="06/2015",
    label="Jun-2015",
    short_name="Jun-2015",
    stratum_id=1,
    id=185001,
    end=datetime(2015, 7, 1),  # NOQA: DTZ001
    parent=p2015_q2,
)
p2015_q3 = Period(
    code="Q3-2015",
    label="Q3-FY15",
    short_name="Q3-FY15",
    stratum_id=2,
    id=62002,
    end=datetime(2015, 10, 1),  # NOQA: DTZ001
    parent=p2015,
)
p2015_jul = Period(
    code="07/2015",
    label="Jul-2015",
    short_name="Jul-2015",
    stratum_id=1,
    id=186001,
    end=datetime(2015, 8, 1),  # NOQA: DTZ001
    parent=p2015_q3,
)
p2015_aug = Period(
    code="08/2015",
    label="Aug-2015",
    short_name="Aug-2015",
    stratum_id=1,
    id=187001,
    end=datetime(2015, 9, 1),  # NOQA: DTZ001
    parent=p2015_q3,
)
p2015_sep = Period(
    code="09/2015",
    label="Sep-2015",
    short_name="Sep-2015",
    stratum_id=1,
    id=188001,
    end=datetime(2015, 10, 1),  # NOQA: DTZ001
    parent=p2015_q3,
)
p2015_q4 = Period(
    code="Q4-2015",
    label="Q4-FY15",
    short_name="Q4-FY15",
    stratum_id=2,
    id=63002,
    end=datetime(2016, 1, 1),  # NOQA: DTZ001
    parent=p2015,
)
p2015_oct = Period(
    code="10/2015",
    label="Oct-2015",
    short_name="Oct-2015",
    stratum_id=1,
    id=189001,
    end=datetime(2015, 11, 1),  # NOQA: DTZ001
    parent=p2015_q4,
)
p2015_nov = Period(
    code="11/2015",
    label="Nov-2015",
    short_name="Nov-2015",
    stratum_id=1,
    id=190001,
    end=datetime(2015, 12, 1),  # NOQA: DTZ001
    parent=p2015_q4,
)
p2015_dec = Period(
    code="12/2015",
    label="Dec-2015",
    short_name="Dec-2015",
    stratum_id=1,
    id=191001,
    end=datetime(2016, 1, 1),  # NOQA: DTZ001
    parent=p2015_q4,
)

p2016 = Period(
    code="2016",
    label="FY2016",
    short_name="FY2016",
    stratum_id=3,
    id=16003,
    end=datetime(2017, 1, 1),  # NOQA: DTZ001
)

p2016_q1 = Period(
    code="Q1-2016",
    label="Q1-FY16",
    short_name="Q1-FY16",
    stratum_id=2,
    id=64002,
    end=datetime(2016, 4, 1),  # NOQA: DTZ001
    parent=p2016,
)
p2016_jan = Period(
    code="01/2016",
    label="Jan-2016",
    short_name="Jan-2016",
    stratum_id=1,
    id=192001,
    end=datetime(2016, 2, 1),  # NOQA: DTZ001
    parent=p2016_q1,
)
p2016_feb = Period(
    code="02/2016",
    label="Feb-2016",
    short_name="Feb-2016",
    stratum_id=1,
    id=193001,
    end=datetime(2016, 3, 1),  # NOQA: DTZ001
    parent=p2016_q1,
)
p2016_mar = Period(
    code="03/2016",
    label="Mar-2016",
    short_name="Mar-2016",
    stratum_id=1,
    id=194001,
    end=datetime(2016, 4, 1),  # NOQA: DTZ001
    parent=p2016_q1,
)
p2016_q2 = Period(
    code="Q2-2016",
    label="Q2-FY16",
    short_name="Q2-FY16",
    stratum_id=2,
    id=65002,
    end=datetime(2016, 7, 1),  # NOQA: DTZ001
    parent=p2016,
)
p2016_apr = Period(
    code="04/2016",
    label="Apr-2016",
    short_name="Apr-2016",
    stratum_id=1,
    id=195001,
    end=datetime(2016, 5, 1),  # NOQA: DTZ001
    parent=p2016_q2,
)
p2016_may = Period(
    code="05/2016",
    label="May-2016",
    short_name="May-2016",
    stratum_id=1,
    id=196001,
    end=datetime(2016, 6, 1),  # NOQA: DTZ001
    parent=p2016_q2,
)
p2016_jun = Period(
    code="06/2016",
    label="Jun-2016",
    short_name="Jun-2016",
    stratum_id=1,
    id=197001,
    end=datetime(2016, 7, 1),  # NOQA: DTZ001
    parent=p2016_q2,
)
p2016_q3 = Period(
    code="Q3-2016",
    label="Q3-FY16",
    short_name="Q3-FY16",
    stratum_id=2,
    id=66002,
    end=datetime(2016, 10, 1),  # NOQA: DTZ001
    parent=p2016,
)
p2016_jul = Period(
    code="07/2016",
    label="Jul-2016",
    short_name="Jul-2016",
    stratum_id=1,
    id=198001,
    end=datetime(2016, 8, 1),  # NOQA: DTZ001
    parent=p2016_q3,
)
p2016_aug = Period(
    code="08/2016",
    label="Aug-2016",
    short_name="Aug-2016",
    stratum_id=1,
    id=199001,
    end=datetime(2016, 9, 1),  # NOQA: DTZ001
    parent=p2016_q3,
)
p2016_sep = Period(
    code="09/2016",
    label="Sep-2016",
    short_name="Sep-2016",
    stratum_id=1,
    id=200001,
    end=datetime(2016, 10, 1),  # NOQA: DTZ001
    parent=p2016_q3,
)
p2016_q4 = Period(
    code="Q4-2016",
    label="Q4-FY16",
    short_name="Q4-FY16",
    stratum_id=2,
    id=67002,
    end=datetime(2017, 1, 1),  # NOQA: DTZ001
    parent=p2016,
)
p2016_oct = Period(
    code="10/2016",
    label="Oct-2016",
    short_name="Oct-2016",
    stratum_id=1,
    id=201001,
    end=datetime(2016, 11, 1),  # NOQA: DTZ001
    parent=p2016_q4,
)
p2016_nov = Period(
    code="11/2016",
    label="Nov-2016",
    short_name="Nov-2016",
    stratum_id=1,
    id=202001,
    end=datetime(2016, 12, 1),  # NOQA: DTZ001
    parent=p2016_q4,
)
p2016_dec = Period(
    code="12/2016",
    label="Dec-2016",
    short_name="Dec-2016",
    stratum_id=1,
    id=203001,
    end=datetime(2017, 1, 1),  # NOQA: DTZ001
    parent=p2016_q4,
)

t1 = Time(
    is_custom=True,
    seq_no="24",
    stratum=MetadataList([s3, s2, s1]),
    period=MetadataList(
        [
            p2015,
            p2015_q1,
            p2015_jan,
            p2015_feb,
            p2015_mar,
            p2015_q2,
            p2015_apr,
            p2015_may,
            p2015_jun,
            p2015_q3,
            p2015_jul,
            p2015_aug,
            p2015_sep,
            p2015_q4,
            p2015_oct,
            p2015_nov,
            p2015_dec,
            p2016,
            p2016_q1,
            p2016_jan,
            p2016_feb,
            p2016_mar,
            p2016_q2,
            p2016_apr,
            p2016_may,
            p2016_jun,
            p2016_q3,
            p2016_jul,
            p2016_aug,
            p2016_sep,
            p2016_q4,
            p2016_oct,
            p2016_nov,
            p2016_dec,
        ],
    ),
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
    <time isCustom="1" seqNo="24">
      <stratum code="year" label="Year" shortName="Yr" id="3" inUse="1">
        <stratum code="qtr" label="Quarter" shortName="Qtr" id="2" inUse="1">
          <stratum code="month" label="Month" shortName="Mon" id="1" inUse="1" isDefault="1" />
        </stratum>
      </stratum>
      <period code="2015" label="FY2015" shortName="FY2015" stratumId="3" timeslot="15" encodedTimePeriod="3::15" id="15003" end="2016-01-01">
        <period code="Q1-2015" label="Q1-FY15" shortName="Q1-FY15" stratumId="2" timeslot="60" encodedTimePeriod="2::60" id="60002" end="2015-04-01">
          <period code="01/2015" label="Jan-2015" shortName="Jan-2015" stratumId="1" timeslot="180" encodedTimePeriod="1::180" id="180001" end="2015-02-01" />
          <period code="02/2015" label="Feb-2015" shortName="Feb-2015" stratumId="1" timeslot="181" encodedTimePeriod="1::181" id="181001" end="2015-03-01" />
          <period code="03/2015" label="Mar-2015" shortName="Mar-2015" stratumId="1" timeslot="182" encodedTimePeriod="1::182" id="182001" end="2015-04-01" />
        </period>
        <period code="Q2-2015" label="Q2-FY15" shortName="Q2-FY15" stratumId="2" timeslot="61" encodedTimePeriod="2::61" id="61002" end="2015-07-01">
          <period code="04/2015" label="Apr-2015" shortName="Apr-2015" stratumId="1" timeslot="183" encodedTimePeriod="1::183" id="183001" end="2015-05-01" />
          <period code="05/2015" label="May-2015" shortName="May-2015" stratumId="1" timeslot="184" encodedTimePeriod="1::184" id="184001" end="2015-06-01" />
          <period code="06/2015" label="Jun-2015" shortName="Jun-2015" stratumId="1" timeslot="185" encodedTimePeriod="1::185" id="185001" end="2015-07-01" />
        </period>
        <period code="Q3-2015" label="Q3-FY15" shortName="Q3-FY15" stratumId="2" timeslot="62" encodedTimePeriod="2::62" id="62002" end="2015-10-01">
          <period code="07/2015" label="Jul-2015" shortName="Jul-2015" stratumId="1" timeslot="186" encodedTimePeriod="1::186" id="186001" end="2015-08-01" />
          <period code="08/2015" label="Aug-2015" shortName="Aug-2015" stratumId="1" timeslot="187" encodedTimePeriod="1::187" id="187001" end="2015-09-01" />
          <period code="09/2015" label="Sep-2015" shortName="Sep-2015" stratumId="1" timeslot="188" encodedTimePeriod="1::188" id="188001" end="2015-10-01" />
        </period>
        <period code="Q4-2015" label="Q4-FY15" shortName="Q4-FY15" stratumId="2" timeslot="63" encodedTimePeriod="2::63" id="63002" end="2016-01-01">
          <period code="10/2015" label="Oct-2015" shortName="Oct-2015" stratumId="1" timeslot="189" encodedTimePeriod="1::189" id="189001" end="2015-11-01" />
          <period code="11/2015" label="Nov-2015" shortName="Nov-2015" stratumId="1" timeslot="190" encodedTimePeriod="1::190" id="190001" end="2015-12-01" />
          <period code="12/2015" label="Dec-2015" shortName="Dec-2015" stratumId="1" timeslot="191" encodedTimePeriod="1::191" id="191001" end="2016-01-01" />
        </period>
      </period>
      <period code="2016" label="FY2016" shortName="FY2016" stratumId="3" timeslot="16" encodedTimePeriod="3::16" id="16003" end="2017-01-01">
        <period code="Q1-2016" label="Q1-FY16" shortName="Q1-FY16" stratumId="2" timeslot="64" encodedTimePeriod="2::64" id="64002" end="2016-04-01">
          <period code="01/2016" label="Jan-2016" shortName="Jan-2016" stratumId="1" timeslot="192" encodedTimePeriod="1::192" id="192001" end="2016-02-01" />
          <period code="02/2016" label="Feb-2016" shortName="Feb-2016" stratumId="1" timeslot="193" encodedTimePeriod="1::193" id="193001" end="2016-03-01" />
          <period code="03/2016" label="Mar-2016" shortName="Mar-2016" stratumId="1" timeslot="194" encodedTimePeriod="1::194" id="194001" end="2016-04-01" />
        </period>
        <period code="Q2-2016" label="Q2-FY16" shortName="Q2-FY16" stratumId="2" timeslot="65" encodedTimePeriod="2::65" id="65002" end="2016-07-01">
          <period code="04/2016" label="Apr-2016" shortName="Apr-2016" stratumId="1" timeslot="195" encodedTimePeriod="1::195" id="195001" end="2016-05-01" />
          <period code="05/2016" label="May-2016" shortName="May-2016" stratumId="1" timeslot="196" encodedTimePeriod="1::196" id="196001" end="2016-06-01" />
          <period code="06/2016" label="Jun-2016" shortName="Jun-2016" stratumId="1" timeslot="197" encodedTimePeriod="1::197" id="197001" end="2016-07-01" />
        </period>
        <period code="Q3-2016" label="Q3-FY16" shortName="Q3-FY16" stratumId="2" timeslot="66" encodedTimePeriod="2::66" id="66002" end="2016-10-01">
          <period code="07/2016" label="Jul-2016" shortName="Jul-2016" stratumId="1" timeslot="198" encodedTimePeriod="1::198" id="198001" end="2016-08-01" />
          <period code="08/2016" label="Aug-2016" shortName="Aug-2016" stratumId="1" timeslot="199" encodedTimePeriod="1::199" id="199001" end="2016-09-01" />
          <period code="09/2016" label="Sep-2016" shortName="Sep-2016" stratumId="1" timeslot="200" encodedTimePeriod="1::200" id="200001" end="2016-10-01" />
        </period>
        <period code="Q4-2016" label="Q4-FY16" shortName="Q4-FY16" stratumId="2" timeslot="67" encodedTimePeriod="2::67" id="67002" end="2017-01-01">
          <period code="10/2016" label="Oct-2016" shortName="Oct-2016" stratumId="1" timeslot="201" encodedTimePeriod="1::201" id="201001" end="2016-11-01" />
          <period code="11/2016" label="Nov-2016" shortName="Nov-2016" stratumId="1" timeslot="202" encodedTimePeriod="1::202" id="202001" end="2016-12-01" />
          <period code="12/2016" label="Dec-2016" shortName="Dec-2016" stratumId="1" timeslot="203" encodedTimePeriod="2::203" id="203001" end="2017-01-01" />
        </period>
      </period>
    </time>
  </output>
</response>""")  # noqa: E501

# Timeslot missing in period?

tests.append(
    (
        xml2,
        MetadataList([t1]),
    ),
)


# From here down, we're using the original testing methodology
@pytest.fixture
def time_service() -> TimeService:
    """Fixture for wdadaptivepy's Time Service.

    Returns:
        wdadaptivepy TimeService

    """
    xml_api_instance = XMLApi("", "")
    return TimeService(xml_api=xml_api_instance)


@pytest.fixture
def mock_time(
    mocker: MockerFixture,
    time_service: TimeService,
) -> ET.Element:
    """Mock Adaptive's response from exportTimes XML API.

    Args:
        mocker: pytest's mocker
        time_service: wdadaptivepy TimeService to mock

    Returns:
        XML Element

    """
    # Create a mock object for the Times
    mocked_levels = mocker.MagicMock()
    mocker.patch.object(
        time_service._TimeService__xml_api,  # noqa: SLF001  # pyright: ignore[reportAttributeAccessIssue]
        "make_xml_request",
        mocked_levels,
    )
    return mocked_levels


@pytest.mark.parametrize(("element", "expected"), tests)
def test_get_all(
    element: ET.Element,
    expected: MetadataList[Time],
    time_service: TimeService,
    mock_time: MagicMock,
) -> None:
    """Tests that wdadaptivepy properly parses Adaptive's exportTimes XML API response.

    Args:
        element: Adaptive's exportTimes XML API response
        expected: wdadaptivepy MetadataList of Times
        time_service: wdadaptivepy TimeService
        mock_time: Mocker for Adaptive's exportTimes XML API response

    """
    # Set the mock object to return a specific response
    mock_time.return_value = element

    # Call the function that downloads data from the external service
    levels = time_service.get_all()

    # Verify that the function returns the expected data
    assert levels == expected


@pytest.mark.parametrize(
    ("element", "expected", "index_with_error", "key_with_error"),
    test_with_errors,
)
def test_get_all_with_errors(  # noqa: PLR0913
    element: ET.Element,
    expected: MetadataList[Time],
    index_with_error: int,
    key_with_error: str,
    time_service: TimeService,
    mock_time: MagicMock,
) -> None:
    """Tests that wdadaptivepy properly parses Adaptive's exportTimes XML API response.

    Args:
        element: Adaptive's exportTimes XML API response
        expected: wdadaptivepy MetadataList of Times
        index_with_error: the item in the MetadataList that shouldn't match
        key_with_error: the key for the property in that item that should't match
        time_service: wdadaptivepy TimeService
        mock_time: Mocker for Adaptive's exportTimes XML API response

    """
    # Set the mock object to return a specific response
    mock_time.return_value = element

    # Call the function that downloads data from the external service
    levels = time_service.get_all()

    # Verify that the function returns the expected data
    xml_value = getattr(levels[index_with_error], key_with_error, None)
    expected_value = getattr(expected[index_with_error], key_with_error, None)
    assert xml_value != expected_value
