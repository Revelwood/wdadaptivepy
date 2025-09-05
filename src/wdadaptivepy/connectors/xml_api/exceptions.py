"""Exceptions for Adaptive XML API."""


class InvalidCredentialsError(Exception):
    """Exception for invalid Adaptive credentials."""


class FailedRequestError(Exception):
    """Exception for unsuccessful XML API calls.

    Attributes:
        method: Adaptive XML API name

    """

    def __init__(self, message: str, method: str) -> None:
        """Generate Exception for unsuccessful XML API calls.

        Args:
            message: Exception message
            method: Adaptive XML API name

        """
        super().__init__(message, method)
        self.method = method
