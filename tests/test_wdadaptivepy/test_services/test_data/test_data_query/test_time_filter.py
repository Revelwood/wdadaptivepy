"""Tests for wdadaptivepy's time_filter from data_query."""

import pytest

from wdadaptivepy.connectors.xml_api.xml_api import XMLApi
from wdadaptivepy.models import Period, Stratum
from wdadaptivepy.models.data import TimeFilter
from wdadaptivepy.services.data import DataQuery


@pytest.fixture
def query() -> DataQuery:
    """Fixture for DataQuery.

    Returns:
        XMLApi

    """
    return DataQuery(XMLApi("", ""))


def test_no_time_filter(query: DataQuery) -> None:
    """Test data query initializes with no time filter.

    Args:
        query: Mocked DataQuery

    """
    assert query.time_filter is None


def test_time_filter_by_string(query: DataQuery) -> None:
    """Test setting time filter by string.

    Args:
        query: Mocked DataQuery

    """
    query.set_time_filter(start_period="2025-01", end_period="2025-06")
    assert query.time_filter == TimeFilter(
        start=Period(code="2025-01"),
        end=Period(code="2025-06"),
        stratum=None,
    )


def test_time_filter_stratum_by_string(query: DataQuery) -> None:
    """Test setting time filter by string with stratum.

    Args:
        query: Mocked DataQuery

    """
    query.set_time_filter(
        start_period="2025-01",
        end_period="2025-06",
        stratum="Year",
    )
    assert query.time_filter == TimeFilter(
        start=Period(code="2025-01"),
        end=Period(code="2025-06"),
        stratum=Stratum(code="Year"),
    )


def test_time_filter_start_and_end_by_model(query: DataQuery) -> None:
    """Test setting time filter by wdadaptivepy models.

    Args:
        query: Mocked DataQuery

    """
    start_period = Period(code="2025-01")
    end_period = Period(code="2025-06")
    query.set_time_filter(
        start_period=start_period,
        end_period=end_period,
    )
    assert query.time_filter == TimeFilter(
        start=start_period, end=end_period, stratum=None
    )


def test_time_filter_by_model(query: DataQuery) -> None:
    """Test setting time filter by wdadaptivepy models with stratum.

    Args:
        query: Mocked DataQuery

    """
    start_period = Period(code="2025-01")
    end_period = Period(code="2025-06")
    stratum = Stratum(code="Year")
    query.set_time_filter(
        start_period=start_period,
        end_period=end_period,
        stratum=stratum,
    )
    assert query.time_filter == TimeFilter(
        start=start_period, end=end_period, stratum=stratum
    )
