"""Tests for wdadaptivepy's model for MetadataList."""

import pytest

from wdadaptivepy.models.base import MetadataAttribute
from wdadaptivepy.models.level import Level
from wdadaptivepy.models.list import MetadataList


def test_successful_get_member() -> None:
    """Test that get_member successfully returns expected matches."""
    set_first = Level(id=1)
    set_second = Level(id=2)
    levels = MetadataList([set_first, set_second])
    found_first = levels.get_member(id=1)
    found_second = levels.get_member(id=2)
    assert set_first == found_first
    assert set_second == found_second


def test_type_coercion_get_member() -> None:
    """Test that get_member successfully handles property type coercion."""
    set_first = Level(id=1)
    set_second = Level(id=2)
    levels = MetadataList([set_first, set_second])
    found_first = levels.get_member(id="1")
    found_second = levels.get_member(id="2")
    assert set_first == found_first
    assert set_second == found_second


def test_invalid_property_get_member() -> None:
    """Test that get_member raises expected Exception for invalid properties."""
    set_first = Level(id=1)
    set_second = Level(id=2)
    levels = MetadataList([set_first, set_second])
    with pytest.raises(expected_exception=ValueError, match=r"^$"):
        levels.get_member(invalid_property="something")


def test_no_match_get_member() -> None:
    """Test that get_member raises expected Exception for no matches."""
    set_first = Level(id=1)
    set_second = Level(id=2)
    levels = MetadataList([set_first, set_second])
    with pytest.raises(expected_exception=ValueError, match=r"^$"):
        levels.get_member(id=3)


def test_no_kwarg_get_member() -> None:
    """Test that get_member raises expected Exception for invalid calls."""
    set_first = Level(id=1)
    set_second = Level(id=2)
    levels = MetadataList([set_first, set_second])
    with pytest.raises(expected_exception=TypeError):
        levels.get_member("id")  # pyright: ignore[reportCallIssue]


def test_first_match_get_member() -> None:
    """Test that get_member always returns the first match."""
    set_first = Level(id=1, code="1", name="First")
    set_second = Level(id=2, code="2", name="First")
    levels = MetadataList([set_first, set_second])
    found_first = levels.get_member(name="First")
    found_second = levels.get_member(name="First")
    assert set_first == found_first
    assert set_first == found_second
    assert set_second != found_first
    assert set_second != found_second


def test_empty_list_get_member() -> None:
    """Test that get_member raises expected Exception for empty MetadataList."""
    levels = MetadataList[Level]()
    with pytest.raises(expected_exception=ValueError, match=r"^$"):
        levels.get_member(id=1)


def test_get_members() -> None:
    """Test that get_members returns the matched members."""
    set_first = Level(id=1, code="1", name="First")
    set_second = Level(id=2, code="2", name="Second")
    set_third = Level(id=3, code="3", name="First")
    levels = MetadataList([set_first, set_second, set_third])
    found = levels.get_members(name="First")
    assert found == MetadataList([set_first, set_third])


def test_adaptive_parent_get_member() -> None:
    """Test that get_member returns matches for adaptive_parent."""
    set_first = Level(id=1, code="1", name="First")
    set_second = Level(id=2, code="2", name="First")
    set_second.set_adaptive_parent(adaptive_parent=set_first)
    set_third = Level(id=3, code="3", name="First")
    set_third.set_adaptive_parent(adaptive_parent=set_second)
    levels = MetadataList([set_first, set_second, set_third])
    # found_third = levels.get_member(adaptive_parent=Level(id=2, code="2", name="First"))
    found_third = levels.get_member(adaptive_parent=levels.get_member(code="2"))
    # found_third = levels.get_member(adaptive_parent=set_second)

    assert set_third == found_third


def test_adaptive_attribute_get_member() -> None:
    """Test that get_member returns matches for adaptive_parent."""
    set_first = Level(id=1, code="1", name="First")
    set_second = Level(id=2, code="2", name="First")
    set_third = Level(id=3, code="3", name="First")
    third_attribute = MetadataAttribute(
        attribute_id=1, name="Test", value_id=2, value="Something"
    )
    set_third.set_adaptive_attribute(third_attribute)
    levels = MetadataList([set_first, set_second, set_third])
    # found_third = levels.get_member(
    #     adaptive_attributes=MetadataAttribute(
    #         attribute_id=1, name="Test", value_id=2, value="Something"
    #     )
    # )
    found_third = levels.get_member(adaptive_attributes=[third_attribute])
    assert set_third == found_third


def test_advanced_get_member() -> None:
    """Test that advanced filter returns member."""
    set_first = Level(id=1, code="1", name="First")
    set_second = Level(id=2, code="2", name="Second")
    set_second.set_adaptive_parent(adaptive_parent=set_first)
    set_third = Level(id=3, code="3", name="Third")
    levels = MetadataList([set_first, set_second, set_third])
    found = list(filter(lambda x: "r" in x.name, levels))
    assert found == [set_first, set_third]
