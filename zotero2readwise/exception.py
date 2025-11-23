"""Custom exceptions for the Zotero2Readwise library.

This module defines custom exception classes used throughout the library
for error handling and reporting.
"""


class Zotero2ReadwiseError(Exception):
    """Base exception class for Zotero2Readwise errors.

    This exception is raised when errors occur during the synchronization
    process, such as API failures or data formatting issues.

    Attributes:
        message: Human-readable error description.

    Example:
        >>> raise Zotero2ReadwiseError("Failed to upload highlights")
        Zotero2ReadwiseError: Failed to upload highlights
    """

    def __init__(self, message: str):
        """Initialize the exception with an error message.

        Args:
            message: Human-readable description of the error.
        """
        self.message = message

        super().__init__(self.message)
