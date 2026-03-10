"""Tests for wdadaptivepy's version_filter from data_query."""

import pytest

from wdadaptivepy.connectors.xml_api.xml_api import XMLApi
from wdadaptivepy.models import Version
from wdadaptivepy.models.data import VersionFilter
from wdadaptivepy.services.data import DataQuery


@pytest.fixture
def query() -> DataQuery:
    """Fixture for DataQuery.

    Returns:
        XMLApi

    """
    return DataQuery(XMLApi("", ""))


def test_no_version_filter(query: DataQuery) -> None:
    """Test data query initializes with an empty version filter.

    Args:
        query: Mocked DataQuery

    """
    assert query.version_filter == VersionFilter(
        version=None,
        is_default=None,
    )


def test_set_version_filter_by_string(query: DataQuery) -> None:
    """Test setting version filter by string.

    Args:
        query: Mocked DataQuery

    """
    query.set_version_filter("Test")
    assert query.version_filter == VersionFilter(
        version=Version(name="Test"),
        is_default=None,
    )


def test_set_version_filter_by_model(query: DataQuery) -> None:
    """Test setting version filter by wdadaptivepy model.

    Args:
        query: Mocked DataQuery

    """
    test_version = Version(name="Test")
    query.set_version_filter(test_version)
    assert query.version_filter == VersionFilter(version=test_version, is_default=None)


def test_set_version_filter_default(query: DataQuery) -> None:
    """Test setting version filter to default version.

    Args:
        query: Mocked DataQuery

    """
    query.set_version_filter(use_default=True)
    assert query.version_filter == VersionFilter(version=None, is_default=True)
