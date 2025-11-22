"""Tests for custom exceptions."""

import pytest

from zotero2readwise.exception import Zotero2ReadwiseError


class TestZotero2ReadwiseError:
    """Tests for Zotero2ReadwiseError exception."""

    def test_exception_creation(self):
        """Test creating exception with message."""
        error_msg = "Test error message"
        error = Zotero2ReadwiseError(error_msg)

        assert error.message == error_msg
        assert str(error) == error_msg

    def test_exception_can_be_raised(self):
        """Test that exception can be raised."""
        with pytest.raises(Zotero2ReadwiseError) as exc_info:
            raise Zotero2ReadwiseError("Something went wrong")

        assert str(exc_info.value) == "Something went wrong"

    def test_exception_inheritance(self):
        """Test that exception inherits from Exception."""
        error = Zotero2ReadwiseError("Test")
        assert isinstance(error, Exception)

    def test_exception_with_empty_message(self):
        """Test exception with empty message."""
        error = Zotero2ReadwiseError("")
        assert error.message == ""
        assert str(error) == ""

    def test_exception_with_unicode_message(self):
        """Test exception with Unicode message."""
        error_msg = "错误: 无法处理中文字符"
        error = Zotero2ReadwiseError(error_msg)
        assert error.message == error_msg
        assert str(error) == error_msg
