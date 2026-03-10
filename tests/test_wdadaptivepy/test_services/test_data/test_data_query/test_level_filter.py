"""Tests for wdadaptivepy's level_filter from data_query."""

import pytest

from wdadaptivepy.connectors.xml_api.xml_api import XMLApi
from wdadaptivepy.models import Level
from wdadaptivepy.models.data import LevelFilter
from wdadaptivepy.services.data import DataQuery


@pytest.fixture
def query() -> DataQuery:
    """Fixture for DataQuery.

    Returns:
        DataQuery

    """
    return DataQuery(XMLApi("", ""))


def test_no_level_filter(query: DataQuery) -> None:
    """Test a data query initializes with no level filters.

    Args:
        query: Mocked DataQuery

    """
    assert query.level_filter == []


def test_level_filter_by_string(query: DataQuery) -> None:
    """Test adding level filter by string.

    Args:
        query: Mocked DataQuery

    """
    query.add_level_filter("Top")
    assert query.level_filter == [
        LevelFilter(level=Level(code="Top"), is_rollup=False, include_descendants=True)
    ]


def test_level_filter_by_model(query: DataQuery) -> None:
    """Test adding level filter by wdadaptivepy model.

    Args:
        query: Mocked DataQuery

    """
    top_level = Level(code="Top")
    query.add_level_filter(top_level)
    assert query.level_filter == [
        LevelFilter(
            level=top_level,
            is_rollup=False,
            include_descendants=True,
        )
    ]


def test_level_filter_by_list_string(query: DataQuery) -> None:
    """Test adding level filter by list of strings.

    Args:
        query: Mocked DataQuery

    """
    levels = ["Top", "Next"]
    query.add_level_filter(levels)
    assert query.level_filter == [
        LevelFilter(
            level=Level(code=levels[0]),
            is_rollup=False,
            include_descendants=True,
        ),
        LevelFilter(
            level=Level(code=levels[1]),
            is_rollup=False,
            include_descendants=True,
        ),
    ]


def test_level_filter_by_list_models(query: DataQuery) -> None:
    """Test adding level filters by list of wdadaptivepy models.

    Args:
        query: Mocked DataQuery

    """
    levels = [Level(code="Top"), Level(code="Next")]
    query.add_level_filter(levels)
    assert query.level_filter == [
        LevelFilter(
            level=levels[0],
            is_rollup=False,
            include_descendants=True,
        ),
        LevelFilter(
            level=levels[1],
            is_rollup=False,
            include_descendants=True,
        ),
    ]


def test_level_filter_is_rollup_true(query: DataQuery) -> None:
    """Test level filter with is_rollup is true.

    Args:
        query: Mocked DataQuery

    """
    query.add_level_filter("Top", is_rollup=True)
    assert query.level_filter == [
        LevelFilter(
            level=Level(code="Top"),
            is_rollup=True,
            include_descendants=True,
        )
    ]


def test_level_filter_is_rollup_false(query: DataQuery) -> None:
    """Test level filter with is_rollup is false.

    Args:
        query: Mocked DataQuery

    """
    query.add_level_filter("Top", is_rollup=False)
    assert query.level_filter == [
        LevelFilter(level=Level(code="Top"), is_rollup=False, include_descendants=True)
    ]


def test_level_filter_include_descendants_true(query: DataQuery) -> None:
    """Test level filter with include_descendants is true.

    Args:
        query: Mocked DataQuery

    """
    query.add_level_filter("Top", include_descendants=True)
    assert query.level_filter == [
        LevelFilter(level=Level(code="Top"), is_rollup=False, include_descendants=True)
    ]


def test_level_filter_include_descentants_false(query: DataQuery) -> None:
    """Test level filter with include_descendants is false.

    Args:
        query: Mocked DataQuery

    """
    query.add_level_filter("Top", include_descendants=False)
    assert query.level_filter == [
        LevelFilter(
            level=Level(code="Top"),
            is_rollup=False,
            include_descendants=False,
        )
    ]


def test_level_filter_clear(query: DataQuery) -> None:
    """Test clearing level filters.

    Args:
        query: Mocked DataQuery

    """
    query.add_level_filter("Top")
    assert query.level_filter != []
    query.clear_level_filter()
    assert query.level_filter == []
