"""Tests for helper functions."""

from unittest.mock import mock_open, patch

from zotero2readwise.helper import (
    read_library_version,
    sanitize_tag,
    write_library_version,
)


class TestSanitizeTag:
    """Tests for sanitize_tag function."""

    def test_sanitize_tag_with_spaces(self):
        """Test sanitizing tag with spaces."""
        assert sanitize_tag(" Machine Learning ") == "Machine_Learning"

    def test_sanitize_tag_multiple_spaces(self):
        """Test sanitizing tag with multiple spaces."""
        assert sanitize_tag("  Deep   Learning  ") == "Deep___Learning"

    def test_sanitize_tag_no_spaces(self):
        """Test sanitizing tag without spaces."""
        assert sanitize_tag("Python") == "Python"

    def test_sanitize_tag_empty(self):
        """Test sanitizing empty tag."""
        assert sanitize_tag("") == ""

    def test_sanitize_tag_only_spaces(self):
        """Test sanitizing tag with only spaces."""
        assert sanitize_tag("   ") == ""

    def test_sanitize_tag_with_special_chars(self):
        """Test sanitizing tag with special characters."""
        assert sanitize_tag(" AI/ML Research ") == "AI/ML_Research"

    def test_sanitize_tag_unicode(self):
        """Test sanitizing tag with Unicode characters."""
        assert sanitize_tag(" 机器 学习 ") == "机器_学习"


class TestReadLibraryVersion:
    """Tests for read_library_version function."""

    def test_read_library_version_file_exists(self, tmp_path):
        """Test reading version when file exists with valid number."""
        since_file = tmp_path / "since"
        since_file.write_text("12345")

        with patch("builtins.open", mock_open(read_data="12345")):
            assert read_library_version() == 12345

    def test_read_library_version_file_not_found(self):
        """Test reading version when file doesn't exist."""
        with patch("builtins.open", side_effect=FileNotFoundError):
            assert read_library_version() == 0

    def test_read_library_version_invalid_content(self):
        """Test reading version when file contains invalid content."""
        with patch("builtins.open", mock_open(read_data="not_a_number")):
            assert read_library_version() == 0

    def test_read_library_version_empty_file(self):
        """Test reading version when file is empty."""
        with patch("builtins.open", mock_open(read_data="")):
            assert read_library_version() == 0

    def test_read_library_version_zero(self):
        """Test reading version when file contains zero."""
        with patch("builtins.open", mock_open(read_data="0")):
            assert read_library_version() == 0


class TestWriteLibraryVersion:
    """Tests for write_library_version function."""

    def test_write_library_version(self, tmp_path, mock_zotero_client):
        """Test writing library version to file."""
        _since_file = tmp_path / "since"  # noqa: F841
        mock_zotero_client.last_modified_version.return_value = 54321

        m = mock_open()
        with patch("builtins.open", m):
            write_library_version(mock_zotero_client)

        m.assert_called_once_with("since", "w", encoding="utf-8")
        m().write.assert_called_once_with("54321")

    def test_write_library_version_zero(self, mock_zotero_client):
        """Test writing zero version."""
        mock_zotero_client.last_modified_version.return_value = 0

        m = mock_open()
        with patch("builtins.open", m):
            write_library_version(mock_zotero_client)

        m().write.assert_called_once_with("0")

    def test_write_library_version_large_number(self, mock_zotero_client):
        """Test writing large version number."""
        mock_zotero_client.last_modified_version.return_value = 999999999

        m = mock_open()
        with patch("builtins.open", m):
            write_library_version(mock_zotero_client)

        m().write.assert_called_once_with("999999999")
