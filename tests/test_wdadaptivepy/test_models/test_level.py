"""Tests for wdadaptivepy's model for Adaptive's Level."""

# import pytest

from wdadaptivepy.models.base import MetadataAttribute
from wdadaptivepy.models.level import Level

# def test_prevent_empty_level() -> None:
#     with pytest.raises(ValueError):
#         empty_level = Level()


def test_child_inherits_parent_changes() -> None:
    """Test that a Level is added as a child when setting the Level's parent."""
    parent = Level(id=1, code="parent", name="parent")
    child = Level(id=2, code="child", name="child")
    child.set_adaptive_parent(parent)
    another_parent = child.adaptive_parent
    assert another_parent is not None
    another_parent.name = "new parent"
    assert parent.name == "new parent"
    assert child.adaptive_parent == parent
    assert child.adaptive_parent is not None
    assert child.adaptive_parent.name == "new parent"


# def test_child_cannot_change_parent_attributes() -> None:
#     parent = Level(id=1, name="parent")
#     child = Level(id=2, parent=parent)
#     with pytest.raises(ValueError):
#         child.adaptive_parent.name = "new parent"


def test_level_from_dict_expansion() -> None:
    """Test that an wdadaptivepy Level is parsed from expanding a Python Dictionary."""
    values = {
        "id": 1,
        "name": "name",
        "code": "code",
    }
    new_level = Level(**values)
    for key, value in values.items():
        assert getattr(new_level, key) == value


def test_level_from_dict() -> None:
    """Test that an wdadaptivepy Level is parsed from a Python Dictionary."""
    values = {
        "id": 1,
        "name": "name",
        "code": "code",
    }
    new_level = Level.from_dict(values)
    for key, value in values.items():
        assert getattr(new_level[0], key) == value


def test_values_forced_type() -> None:
    """Test that values for an wdadaptivepy Level are forced to correct data type."""
    values = {
        "id": "1",
        "name": "name",
        "code": "code",
    }
    new_level = Level(**values)  # pyright: ignore[reportArgumentType]
    assert new_level.id is not None
    assert isinstance(new_level.id, int)
    assert new_level.id == 1


def test_remove_attribute_returns_new() -> None:
    """Test that removing an attribute does not modify the existing Attribute object."""
    adaptive_attribute = MetadataAttribute(
        attribute_id=1, name="Test", value_id=2, value="Test Value"
    )
    level = Level(id=1)
    level.set_adaptive_attribute(adaptive_attribute=adaptive_attribute)
    assert level.adaptive_attributes[0] == adaptive_attribute

    level.remove_adaptive_attribute(adaptive_attribute_id=1)
    assert level.adaptive_attributes[0] != adaptive_attribute
    assert level.adaptive_attributes[0].value_id == "0"
    assert adaptive_attribute.value_id == "2"
