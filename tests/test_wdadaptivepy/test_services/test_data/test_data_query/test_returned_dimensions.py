"""Tests for wdadaptivepy's returned_dimensions from data_query."""

import pytest

from wdadaptivepy.connectors.xml_api.xml_api import XMLApi
from wdadaptivepy.models import Dimension
from wdadaptivepy.services.data import DataQuery


@pytest.fixture
def query() -> DataQuery:
    """Fixture for DataQuery.

    Returns:
        XMLApi

    """
    return DataQuery(XMLApi("", ""))


def test_returned_dimension_by_string(query: DataQuery) -> None:
    """Test adding returned_dimensions by string.

    Args:
        query: Mocked DataQuery

    """
    query.add_returned_dimension("Supplier")
    assert query.returned_dimensions == ["Supplier"]


def test_returned_dimension_by_model(query: DataQuery) -> None:
    """Test adding returned dimensions by wdadaptivepy model.

    Args:
        query: Mocked DataQuery

    """
    supplier = Dimension(name="Supplier")
    query.add_returned_dimension(supplier)
    assert query.returned_dimensions == [supplier.name]


def test_returned_dimension_by_list_string(query: DataQuery) -> None:
    """Test adding returned dimensions by list of strings.

    Args:
        query: Mocked DataQuery

    """
    dimensions = ["Supplier", "Customer"]
    query.add_returned_dimension(dimensions)
    assert query.returned_dimensions == dimensions


def test_returned_dimension_by_list_model(query: DataQuery) -> None:
    """Test adding returned dimensions by list of wdadaptivepy models.

    Args:
        query: Mocked DataQuery

    """
    dimensions = [Dimension(name="Supplier"), Dimension(name="Customer")]
    query.add_returned_dimension(dimensions)
    assert query.returned_dimensions == [dimension.name for dimension in dimensions]


def test_returned_dimension_with_dimension_values(query: DataQuery) -> None:
    """Test returned dimensions includes dimensions from dimension value filter.

    Args:
        query: Mocked DataQuery

    """
    query.add_dimension_value_filter("Supplier", "Test")
    query.add_returned_dimension("Customer")
    assert query.returned_dimensions == [
        "Supplier",
        "Customer",
    ]
