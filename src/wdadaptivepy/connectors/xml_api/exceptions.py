"""Exceptions for Adaptive XML API."""


class InvalidCredentialsError(Exception):
    """Exception for invalid Adaptive credentials."""


class FailedRequestError(Exception):
    """Exception for unsuccessful XML API calls.

    Attributes:
        method: Adaptive XML API name

    """

    def __init__(self, message: list[dict[str, str | None]], method: str) -> None:
        """Generate Exception for unsuccessful XML API calls.

        Args:
            message: Exception message
            method: Adaptive XML API name

        """
        error_message = "The API request failed to complete successfully"
        if message:
            error_message = str(message)
        super().__init__(error_message, method)
        self.method = method
