"""Tests for wdadaptivepy's main module."""

import pytest

from wdadaptivepy import AdaptiveConnection


def test_connection_requires_login() -> None:
    """Test that wdadaptivepy raises an Exception for missing an Adaptive login."""
    with pytest.raises(TypeError):
        AdaptiveConnection(password="test_password")  # pyright: ignore[reportCallIssue] # noqa: S106


def test_connection_requires_password() -> None:
    """Test that wdadaptivepy raises an Exception for missing an Adaptive password."""
    with pytest.raises(TypeError):
        AdaptiveConnection(login="test_login")  # pyright: ignore[reportCallIssue]


def test_services_existence() -> None:
    """Test that each wdadaptivepy service is properly imported."""
    adaptive = AdaptiveConnection(
        login="test_login",
        password="test_password",  # noqa: S106
        xml_api_version=40,
    )

    services = [
        "accounts",
        "attributes",
        "currencies",
        "dimensions",
        "groups",
        "levels",
        "time",
        "users",
        "versions",
    ]

    for service in services:
        getattr(adaptive, service)
