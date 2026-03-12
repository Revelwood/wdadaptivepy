"""Tests for wdadaptivepy's account_filter from data_query."""

import pytest

from wdadaptivepy.connectors.xml_api.xml_api import XMLApi
from wdadaptivepy.models import Account
from wdadaptivepy.models.data import AccountFilter
from wdadaptivepy.services.data import DataQuery


@pytest.fixture
def query() -> DataQuery:
    """Fixture for DataQuery tests.

    Returns:
        DataQuery

    """
    return DataQuery(XMLApi("", ""))


def test_no_account_filter(query: DataQuery) -> None:
    """Test that a DataQuery initializes with no account filters.

    Args:
        query: Mocked DataQuery

    """
    assert query.account_filter == []


def test_account_filter_by_string(query: DataQuery) -> None:
    """Test an account filter using codes as string.

    Args:
        query: Mocked DataQuery

    """
    query.add_account_filter("Asset")
    assert query.account_filter == [
        AccountFilter(
            account=Account(
                code="Asset",
                is_assumption=False,
            ),
            include_descendants=True,
        )
    ]


def test_account_filter_by_model(query: DataQuery) -> None:
    """Test an account filter using wdadaptivepy models.

    Args:
        query: Mocked DataQuery

    """
    test_account = Account(code="Asset", is_assumption=False)
    query.add_account_filter(test_account)
    assert query.account_filter == [
        AccountFilter(
            account=Account(
                code="Asset",
                is_assumption=False,
            ),
            include_descendants=True,
        )
    ]


def test_account_filter_include_descendants(query: DataQuery) -> None:
    """Test an account filter respects the include descendants parameter.

    Args:
        query: Mocked DataQuery

    """
    query.add_account_filter("Asset", include_descendants=True)
    assert query.account_filter == [
        AccountFilter(
            account=Account(
                code="Asset",
                is_assumption=False,
            ),
            include_descendants=True,
        )
    ]


def test_account_filter_exclude_descendants(query: DataQuery) -> None:
    """Test an account filter will exclude descendants.

    Args:
        query: Mocked DataQuery

    """
    query.add_account_filter("Asset", include_descendants=False)
    assert query.account_filter == [
        AccountFilter(
            account=Account(code="Asset", is_assumption=False),
            include_descendants=False,
        )
    ]


def test_account_filter_by_list_string(query: DataQuery) -> None:
    """Test account filters using list of strings of codes.

    Args:
        query: Mocked DataQuery

    """
    accounts = ["Asset", "Liability"]
    query.add_account_filter(accounts)
    assert query.account_filter == [
        AccountFilter(
            account=Account(code=accounts[0], is_assumption=False),
            include_descendants=True,
        ),
        AccountFilter(
            account=Account(code=accounts[1], is_assumption=False),
            include_descendants=True,
        ),
    ]


def test_account_filter_by_list_model(query: DataQuery) -> None:
    """Test account filters using list of wdadaptivepy models.

    Args:
        query: Mocked DataQuery

    """
    accounts = [
        Account(code="Asset", is_assumption=False),
        Account(code="Liability", is_assumption=True),
    ]
    query.add_account_filter(accounts)
    assert query.account_filter == [
        AccountFilter(
            account=Account(
                code="Asset",
                is_assumption=False,
            ),
            include_descendants=True,
        ),
        AccountFilter(
            Account(
                code="Liability",
                is_assumption=True,
            ),
            include_descendants=True,
        ),
    ]


def test_account_filter_add_individually(query: DataQuery) -> None:
    """Test adding account filters individually.

    Args:
        query: Mocked DataQuery

    """
    accounts = ["Asset", "Liability"]
    query.add_account_filter(accounts[0])
    query.add_account_filter(accounts[1])
    assert query.account_filter == [
        AccountFilter(
            account=Account(code=accounts[0], is_assumption=False),
            include_descendants=True,
        ),
        AccountFilter(
            account=Account(code=accounts[1], is_assumption=False),
            include_descendants=True,
        ),
    ]


def test_account_filter_clear(query: DataQuery) -> None:
    """Test clearing the account filters.

    Args:
        query: Mocked DataQuery

    """
    query.add_account_filter("Asset")
    assert query.account_filter != []
    query.clear_account_filter()
    assert query.account_filter == []
