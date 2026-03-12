"""Tests for wdadaptivepy's dimension_value_filter from data_query."""

import pytest

from wdadaptivepy.connectors.xml_api.xml_api import XMLApi
from wdadaptivepy.models import Dimension, DimensionValue
from wdadaptivepy.models.data import DimensionValueFilter
from wdadaptivepy.services.data import DataQuery


@pytest.fixture
def query() -> DataQuery:
    """Fixture for DataQuery.

    Returns:
        DataQuery

    """
    return DataQuery(XMLApi("", ""))


def test_no_dimension_value_filter(query: DataQuery) -> None:
    """Test that a data query initializes with no dimension value filters.

    Args:
        query: Mocked DataQuery

    """
    assert query.dimension_value_filter == []


def test_dimension_value_filter_by_string(query: DataQuery) -> None:
    """Test adding a dimension value filter by string.

    Args:
        query: Mocked DataQuery

    """
    query.add_dimension_value_filter(
        dimension="Supplier",
        dimension_values="Test",
    )
    assert query.dimension_value_filter == [
        DimensionValueFilter(
            dimension=Dimension(name="Supplier"),
            dimension_value=DimensionValue(code="Test"),
            uncategorized=None,
            direct_children=None,
            uncategorized_of_dimension=None,
            direct_children_of_dimension=None,
        )
    ]


def test_dimension_value_filter_by_model(query: DataQuery) -> None:
    """Test adding a dimension value filter by wdadaptivepy model.

    Args:
        query: Mocked DataQuery

    """
    supplier_dimension = Dimension(name="Supplier")
    supplier = DimensionValue(code="Test")
    query.add_dimension_value_filter(
        dimension=supplier_dimension,
        dimension_values=supplier,
    )
    assert query.dimension_value_filter == [
        DimensionValueFilter(
            dimension=supplier_dimension,
            dimension_value=supplier,
            uncategorized=None,
            direct_children=None,
            uncategorized_of_dimension=None,
            direct_children_of_dimension=None,
        )
    ]


def test_dimension_value_filter_by_list_strings(query: DataQuery) -> None:
    """Test adding dimension value filters by list of strings.

    Args:
        query: Mocked DataQuery

    """
    query.add_dimension_value_filter(
        dimension="Supplier",
        dimension_values=["Test", "Other"],
    )
    assert query.dimension_value_filter == [
        DimensionValueFilter(
            dimension=Dimension(name="Supplier"),
            dimension_value=DimensionValue(code="Test"),
            uncategorized=None,
            direct_children=None,
            uncategorized_of_dimension=None,
            direct_children_of_dimension=None,
        ),
        DimensionValueFilter(
            dimension=Dimension(name="Supplier"),
            dimension_value=DimensionValue(code="Other"),
            uncategorized=None,
            direct_children=None,
            uncategorized_of_dimension=None,
            direct_children_of_dimension=None,
        ),
    ]


def test_dimension_value_filter_include_direct_children(query: DataQuery) -> None:
    """Test a dimension value filter includes direct children.

    Args:
        query: Mocked DataQuery

    """
    query.add_dimension_value_filter(
        dimension="Supplier",
        dimension_values="Test",
        direct_children=True,
    )
    assert query.dimension_value_filter == [
        DimensionValueFilter(
            dimension=Dimension(name="Supplier"),
            dimension_value=DimensionValue(code="Test"),
            uncategorized=None,
            direct_children=True,
            uncategorized_of_dimension=None,
            direct_children_of_dimension=None,
        )
    ]


def test_dimension_value_filter_exclude_direct_children(query: DataQuery) -> None:
    """Test a dimension value filter excludes direct children.

    Args:
        query: Mocked DataQuery

    """
    query.add_dimension_value_filter(
        dimension="Supplier",
        dimension_values="Test",
        direct_children=False,
    )
    assert query.dimension_value_filter == [
        DimensionValueFilter(
            dimension=Dimension(name="Supplier"),
            dimension_value=DimensionValue(code="Test"),
            uncategorized=None,
            direct_children=False,
            uncategorized_of_dimension=None,
            direct_children_of_dimension=None,
        )
    ]


def test_dimension_value_filter_include_uncategorized(query: DataQuery) -> None:
    """Test a dimension value filter includes uncategorized.

    Args:
        query: Mocked DataQuery

    """
    query.add_dimension_value_filter(
        dimension="Supplier",
        dimension_values="Test",
        uncategorized=True,
    )
    assert query.dimension_value_filter == [
        DimensionValueFilter(
            dimension=Dimension(name="Supplier"),
            dimension_value=DimensionValue(code="Test"),
            uncategorized=True,
            direct_children=None,
            uncategorized_of_dimension=None,
            direct_children_of_dimension=None,
        )
    ]


def test_dimension_value_filter_exclude_uncategorized(query: DataQuery) -> None:
    """Test dimension value filter excludes uncategorized.

    Args:
        query: Mocked DataQuery

    """
    query.add_dimension_value_filter(
        dimension="Supplier",
        dimension_values="Test",
        uncategorized=False,
    )
    assert query.dimension_value_filter == [
        DimensionValueFilter(
            dimension=Dimension(name="Supplier"),
            dimension_value=DimensionValue(code="Test"),
            uncategorized=False,
            direct_children=None,
            uncategorized_of_dimension=None,
            direct_children_of_dimension=None,
        )
    ]


def test_dimension_value_filter_clear(query: DataQuery) -> None:
    """Test clearing the dimension value filters.

    Args:
        query: Mocked DataQuery

    """
    query.add_dimension_value_filter(
        dimension="Supplier",
        dimension_values="Test",
    )
    assert query.dimension_value_filter != []
    query.clear_dimension_value_filter()
    assert query.dimension_value_filter == []


def test_dimension_value_filter_uncategorized_of_dimension_model(
    query: DataQuery,
) -> None:
    """Test adding uncategorized of dimension.

    Args:
        query: Mocked DataQuery

    """
    supplier = Dimension(id=123, name="Test")
    query.add_uncategorized_dimension_filter(supplier)
    assert query.dimension_value_filter == [
        DimensionValueFilter(
            dimension=None,
            dimension_value=None,
            uncategorized=None,
            direct_children=None,
            uncategorized_of_dimension=supplier,
            direct_children_of_dimension=None,
        )
    ]


def test_dimension_value_filter_direct_children_of_dimension_model(
    query: DataQuery,
) -> None:
    """Test adding direct children of dimension.

    Args:
        query: Mocked DataQuery

    """
    supplier = Dimension(id=123, name="Supplier")
    query.add_direct_children_of_dimension_filter(supplier)
    assert query.dimension_value_filter == [
        DimensionValueFilter(
            dimension=None,
            dimension_value=None,
            direct_children=None,
            uncategorized=None,
            uncategorized_of_dimension=None,
            direct_children_of_dimension=supplier,
        )
    ]
