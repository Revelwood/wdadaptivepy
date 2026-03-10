"""Tests for wdadaptivepy's data_query."""

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


def test_data_query_initialization(query: DataQuery) -> None:
    """Test the DataQuery object initializes successfully.

    Args:
        query: Mocked DataQuery

    """
    assert query is not None
