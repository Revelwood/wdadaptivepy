"""Tests for wdadaptivepy's XMLAPI class."""

import pytest

from wdadaptivepy.connectors.xml_api.xml_api import XMLApi


def test_connection_requires_login() -> None:
    """Test that wdadaptivepy requires an Adaptive login value."""
    with pytest.raises(TypeError):
        XMLApi(password="test_password")  # pyright: ignore[reportCallIssue] # noqa: S106


def test_connection_requires_password() -> None:
    """Test that wdadaptivepy requires an Adaptive password value."""
    with pytest.raises(TypeError):
        XMLApi(login="test_login")  # pyright: ignore[reportCallIssue]


# def test_unsupported_xml_api_version() -> None:
#     with pytest.raises(ValueError):
#         XMLApi(login="test_login", password="test_password", version=20000)
#     with pytest.raises(ValueError):
#         XMLApi(login="test_login", password="test_password", version=2)
