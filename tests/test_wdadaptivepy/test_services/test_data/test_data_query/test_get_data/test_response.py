"""Test DataQuery's get_data's response parsing."""

from xml.etree import ElementTree as ET

import pytest

from wdadaptivepy.connectors.xml_api.xml_api import XMLApi
from wdadaptivepy.services.data import DataQuery


@pytest.fixture
def query() -> DataQuery:
    """Fixture for DataQuery.

    Returns:
        DataQuery

    """
    return DataQuery(XMLApi("", ""))


@pytest.mark.parametrize(
    ("response_xml", "expected_parsed_response"),
    [
        pytest.param(
            ET.fromstring(
                '<?xml version="1.0" encoding="UTF-8"?>\n'
                "<response>\n"
                '  <output><![CDATA[Account Name,Account Code,Level Code,Level Name,"Location Code","Location Name","Project Code","Project Name","Vendor Code","Vendor Name","Customer Code","Customer Name",01/2026,02/2026,03/2026\n'  # noqa: E501
                '"Assets","1000","100","Marketing","Remote","Remote","None","None","10000","WidgetCo","None","None",0.0,10.0,0.0\n'
                '"Liabilities","2000","200","Accounting","North","North","None","None","None","None","None","None",-1869.3,0.0,0.0\n'
                '"Revenue","4000","300","R&D","None","None","None","None","None","None","20000","MainCo",B,12.34,56.78]]></output>\n'
                '  <status success="true" rowCountSent="3" />\n'
                "</response>\n"
                ""
            ),
            [
                {
                    "Account Code": "1000",
                    "Account Name": "Assets",
                    "Amount": 0.0,
                    "Customer Code": "None",
                    "Customer Name": "None",
                    "Level Code": "100",
                    "Level Name": "Marketing",
                    "Location Code": "Remote",
                    "Location Name": "Remote",
                    "Period Code": "01/2026",
                    "Project Code": "None",
                    "Project Name": "None",
                    "Vendor Code": "10000",
                    "Vendor Name": "WidgetCo",
                },
                {
                    "Account Code": "1000",
                    "Account Name": "Assets",
                    "Amount": 10.0,
                    "Customer Code": "None",
                    "Customer Name": "None",
                    "Level Code": "100",
                    "Level Name": "Marketing",
                    "Location Code": "Remote",
                    "Location Name": "Remote",
                    "Period Code": "02/2026",
                    "Project Code": "None",
                    "Project Name": "None",
                    "Vendor Code": "10000",
                    "Vendor Name": "WidgetCo",
                },
                {
                    "Account Code": "1000",
                    "Account Name": "Assets",
                    "Amount": 0.0,
                    "Customer Code": "None",
                    "Customer Name": "None",
                    "Level Code": "100",
                    "Level Name": "Marketing",
                    "Location Code": "Remote",
                    "Location Name": "Remote",
                    "Period Code": "03/2026",
                    "Project Code": "None",
                    "Project Name": "None",
                    "Vendor Code": "10000",
                    "Vendor Name": "WidgetCo",
                },
                {
                    "Account Code": "2000",
                    "Account Name": "Liabilities",
                    "Amount": -1869.3,
                    "Customer Code": "None",
                    "Customer Name": "None",
                    "Level Code": "200",
                    "Level Name": "Accounting",
                    "Location Code": "North",
                    "Location Name": "North",
                    "Period Code": "01/2026",
                    "Project Code": "None",
                    "Project Name": "None",
                    "Vendor Code": "None",
                    "Vendor Name": "None",
                },
                {
                    "Account Code": "2000",
                    "Account Name": "Liabilities",
                    "Amount": 0.0,
                    "Customer Code": "None",
                    "Customer Name": "None",
                    "Level Code": "200",
                    "Level Name": "Accounting",
                    "Location Code": "North",
                    "Location Name": "North",
                    "Period Code": "02/2026",
                    "Project Code": "None",
                    "Project Name": "None",
                    "Vendor Code": "None",
                    "Vendor Name": "None",
                },
                {
                    "Account Code": "2000",
                    "Account Name": "Liabilities",
                    "Amount": 0.0,
                    "Customer Code": "None",
                    "Customer Name": "None",
                    "Level Code": "200",
                    "Level Name": "Accounting",
                    "Location Code": "North",
                    "Location Name": "North",
                    "Period Code": "03/2026",
                    "Project Code": "None",
                    "Project Name": "None",
                    "Vendor Code": "None",
                    "Vendor Name": "None",
                },
                {
                    "Account Code": "4000",
                    "Account Name": "Revenue",
                    "Amount": None,
                    "Customer Code": "20000",
                    "Customer Name": "MainCo",
                    "Level Code": "300",
                    "Level Name": "R&D",
                    "Location Code": "None",
                    "Location Name": "None",
                    "Period Code": "01/2026",
                    "Project Code": "None",
                    "Project Name": "None",
                    "Vendor Code": "None",
                    "Vendor Name": "None",
                },
                {
                    "Account Code": "4000",
                    "Account Name": "Revenue",
                    "Amount": 12.34,
                    "Customer Code": "20000",
                    "Customer Name": "MainCo",
                    "Level Code": "300",
                    "Level Name": "R&D",
                    "Location Code": "None",
                    "Location Name": "None",
                    "Period Code": "02/2026",
                    "Project Code": "None",
                    "Project Name": "None",
                    "Vendor Code": "None",
                    "Vendor Name": "None",
                },
                {
                    "Account Code": "4000",
                    "Account Name": "Revenue",
                    "Amount": 56.78,
                    "Customer Code": "20000",
                    "Customer Name": "MainCo",
                    "Level Code": "300",
                    "Level Name": "R&D",
                    "Location Code": "None",
                    "Location Name": "None",
                    "Period Code": "03/2026",
                    "Project Code": "None",
                    "Project Name": "None",
                    "Vendor Code": "None",
                    "Vendor Name": "None",
                },
            ],
            id="test_response_with_dimensions",
        ),
        pytest.param(
            ET.fromstring(
                '<?xml version="1.0" encoding="UTF-8"?>\n'
                "<response>\n"
                "  <output><![CDATA[Account Name,Account Code,Level Code,Level Name,Rollup\n"  # noqa: E501
                '"Assets","1000","100","Marketing",0.0\n'
                '"Revenue","4000","300","R&D",B]]></output>\n'
                '  <status success="true" rowCountSent="2" />\n'
                "</response>\n"
                ""
            ),
            [
                {
                    "Account Code": "1000",
                    "Account Name": "Assets",
                    "Amount": 0.0,
                    "Level Code": "100",
                    "Level Name": "Marketing",
                    "Period Code": "Rollup",
                },
                {
                    "Account Code": "4000",
                    "Account Name": "Revenue",
                    "Amount": None,
                    "Level Code": "300",
                    "Level Name": "R&D",
                    "Period Code": "Rollup",
                },
            ],
            id="test_response_time_rollup",
        ),
    ],
)
def test_data_query_response_xml(
    query: DataQuery,
    response_xml: ET.Element,
    expected_parsed_response: list[dict[str, str | float | int]],
) -> None:
    """Test that the XML response is parsed properly."""
    actual_parsed_response = query._parse_response(response_xml)  # noqa: SLF001
    assert actual_parsed_response == expected_parsed_response
