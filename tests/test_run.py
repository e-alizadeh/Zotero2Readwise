"""Tests for CLI run module."""

from unittest.mock import Mock, patch

import pytest

from zotero2readwise.run import main, strtobool


class TestStrtobool:
    """Tests for strtobool function."""

    @pytest.mark.parametrize(
        "value",
        ["y", "Y", "yes", "YES", "Yes", "t", "T", "true", "TRUE", "True", "on", "ON", "1"],
    )
    def test_truthy_values(self, value):
        """Test that truthy string values return 1."""
        assert strtobool(value) == 1

    @pytest.mark.parametrize(
        "value",
        ["n", "N", "no", "NO", "No", "f", "F", "false", "FALSE", "False", "off", "OFF", "0"],
    )
    def test_falsy_values(self, value):
        """Test that falsy string values return 0."""
        assert strtobool(value) == 0

    def test_invalid_value(self):
        """Test that invalid values raise ValueError."""
        with pytest.raises(ValueError, match="invalid truth value"):
            strtobool("invalid")

    def test_empty_string(self):
        """Test that empty string raises ValueError."""
        with pytest.raises(ValueError, match="invalid truth value"):
            strtobool("")

    def test_random_string(self):
        """Test that random strings raise ValueError."""
        with pytest.raises(ValueError, match="invalid truth value"):
            strtobool("maybe")


class TestMainFunction:
    """Tests for main CLI function."""

    @patch("zotero2readwise.run.Zotero2Readwise")
    @patch("zotero2readwise.run.read_library_version")
    @patch("zotero2readwise.run.write_library_version")
    def test_main_with_positional_args(
        self, mock_write_version, mock_read_version, mock_zt2rw
    ):
        """Test main function with positional arguments."""
        mock_instance = Mock()
        mock_zt2rw.return_value = mock_instance
        mock_read_version.return_value = 0

        with patch(
            "sys.argv",
            ["run", "test_readwise_token", "test_zotero_key", "test_library_id"],
        ):
            main()

        mock_zt2rw.assert_called_once()
        call_kwargs = mock_zt2rw.call_args[1]
        assert call_kwargs["readwise_token"] == "test_readwise_token"
        assert call_kwargs["zotero_key"] == "test_zotero_key"
        assert call_kwargs["zotero_library_id"] == "test_library_id"
        mock_instance.run.assert_called_once()

    @patch("zotero2readwise.run.Zotero2Readwise")
    @patch("zotero2readwise.run.read_library_version")
    @patch.dict(
        "os.environ",
        {
            "READWISE_TOKEN": "env_readwise_token",
            "ZOTERO_KEY": "env_zotero_key",
            "ZOTERO_LIBRARY_ID": "env_library_id",
        },
    )
    def test_main_with_environment_variables(self, mock_read_version, mock_zt2rw):
        """Test main function with environment variables."""
        mock_instance = Mock()
        mock_zt2rw.return_value = mock_instance
        mock_read_version.return_value = 0

        with patch("sys.argv", ["run"]):
            main()

        call_kwargs = mock_zt2rw.call_args[1]
        assert call_kwargs["readwise_token"] == "env_readwise_token"
        assert call_kwargs["zotero_key"] == "env_zotero_key"
        assert call_kwargs["zotero_library_id"] == "env_library_id"

    @patch("zotero2readwise.run.Zotero2Readwise")
    @patch("zotero2readwise.run.read_library_version")
    def test_main_with_include_annotations_yes(self, mock_read_version, mock_zt2rw):
        """Test main function with --include_annotations=y."""
        mock_instance = Mock()
        mock_zt2rw.return_value = mock_instance
        mock_read_version.return_value = 0

        with patch(
            "sys.argv",
            [
                "run",
                "token",
                "key",
                "id",
                "--include_annotations",
                "y",
            ],
        ):
            main()

        call_kwargs = mock_zt2rw.call_args[1]
        assert call_kwargs["include_annotations"] is True

    @patch("zotero2readwise.run.Zotero2Readwise")
    @patch("zotero2readwise.run.read_library_version")
    def test_main_with_include_annotations_no(self, mock_read_version, mock_zt2rw):
        """Test main function with --include_annotations=n."""
        mock_instance = Mock()
        mock_zt2rw.return_value = mock_instance
        mock_read_version.return_value = 0

        with patch(
            "sys.argv",
            [
                "run",
                "token",
                "key",
                "id",
                "--include_annotations",
                "n",
            ],
        ):
            main()

        call_kwargs = mock_zt2rw.call_args[1]
        assert call_kwargs["include_annotations"] is False

    @patch("zotero2readwise.run.Zotero2Readwise")
    @patch("zotero2readwise.run.read_library_version")
    def test_main_with_include_notes(self, mock_read_version, mock_zt2rw):
        """Test main function with --include_notes=y."""
        mock_instance = Mock()
        mock_zt2rw.return_value = mock_instance
        mock_read_version.return_value = 0

        with patch(
            "sys.argv",
            [
                "run",
                "token",
                "key",
                "id",
                "--include_notes",
                "y",
            ],
        ):
            main()

        call_kwargs = mock_zt2rw.call_args[1]
        assert call_kwargs["include_notes"] is True

    @patch("zotero2readwise.run.Zotero2Readwise")
    @patch("zotero2readwise.run.read_library_version")
    def test_main_with_filter_colors(self, mock_read_version, mock_zt2rw):
        """Test main function with --filter_color."""
        mock_instance = Mock()
        mock_zt2rw.return_value = mock_instance
        mock_read_version.return_value = 0

        with patch(
            "sys.argv",
            [
                "run",
                "token",
                "key",
                "id",
                "--filter_color",
                "#ffd400",
                "--filter_color",
                "#ff6666",
            ],
        ):
            main()

        call_kwargs = mock_zt2rw.call_args[1]
        assert call_kwargs["filter_colors"] == ("#ffd400", "#ff6666")

    @patch("zotero2readwise.run.Zotero2Readwise")
    @patch("zotero2readwise.run.read_library_version")
    def test_main_with_filter_tags(self, mock_read_version, mock_zt2rw):
        """Test main function with --filter_tags."""
        mock_instance = Mock()
        mock_zt2rw.return_value = mock_instance
        mock_read_version.return_value = 0

        with patch(
            "sys.argv",
            [
                "run",
                "token",
                "key",
                "id",
                "--filter_tags",
                "important",
                "--filter_tags",
                "review",
            ],
        ):
            main()

        call_kwargs = mock_zt2rw.call_args[1]
        assert call_kwargs["filter_tags"] == ("important", "review")

    @patch("zotero2readwise.run.Zotero2Readwise")
    @patch("zotero2readwise.run.read_library_version")
    def test_main_with_include_filter_tags(self, mock_read_version, mock_zt2rw):
        """Test main function with --include_filter_tags."""
        mock_instance = Mock()
        mock_zt2rw.return_value = mock_instance
        mock_read_version.return_value = 0

        with patch(
            "sys.argv",
            [
                "run",
                "token",
                "key",
                "id",
                "--include_filter_tags",
            ],
        ):
            main()

        call_kwargs = mock_zt2rw.call_args[1]
        assert call_kwargs["include_filter_tags"] is True

    @patch("zotero2readwise.run.Zotero2Readwise")
    @patch("zotero2readwise.run.read_library_version")
    @patch("zotero2readwise.run.write_library_version")
    def test_main_with_use_since(
        self, mock_write_version, mock_read_version, mock_zt2rw
    ):
        """Test main function with --use_since."""
        mock_instance = Mock()
        mock_zt2rw.return_value = mock_instance
        mock_read_version.return_value = 12345

        with patch(
            "sys.argv",
            ["run", "token", "key", "id", "--use_since"],
        ):
            main()

        mock_read_version.assert_called_once()
        call_kwargs = mock_zt2rw.call_args[1]
        assert call_kwargs["since"] == 12345
        mock_write_version.assert_called_once_with(mock_instance.zotero_client)

    @patch("zotero2readwise.run.Zotero2Readwise")
    @patch("zotero2readwise.run.read_library_version")
    def test_main_with_suppress_failures(self, mock_read_version, mock_zt2rw):
        """Test main function with --suppress_failures."""
        mock_instance = Mock()
        mock_zt2rw.return_value = mock_instance
        mock_read_version.return_value = 0

        with patch(
            "sys.argv",
            ["run", "token", "key", "id", "--suppress_failures"],
        ):
            main()

        call_kwargs = mock_zt2rw.call_args[1]
        assert call_kwargs["write_failures"] is False

    @patch("zotero2readwise.run.Zotero2Readwise")
    @patch("zotero2readwise.run.read_library_version")
    def test_main_with_custom_tag(self, mock_read_version, mock_zt2rw):
        """Test main function with --custom_tag."""
        mock_instance = Mock()
        mock_zt2rw.return_value = mock_instance
        mock_read_version.return_value = 0

        with patch(
            "sys.argv",
            ["run", "token", "key", "id", "--custom_tag", "zotero"],
        ):
            main()

        call_kwargs = mock_zt2rw.call_args[1]
        assert call_kwargs["custom_tag"] == "zotero"

    @patch("zotero2readwise.run.Zotero2Readwise")
    @patch("zotero2readwise.run.read_library_version")
    def test_main_with_library_type_group(self, mock_read_version, mock_zt2rw):
        """Test main function with --library_type=group."""
        mock_instance = Mock()
        mock_zt2rw.return_value = mock_instance
        mock_read_version.return_value = 0

        with patch(
            "sys.argv",
            ["run", "token", "key", "id", "--library_type", "group"],
        ):
            main()

        call_kwargs = mock_zt2rw.call_args[1]
        assert call_kwargs["zotero_library_type"] == "group"

    def test_main_missing_readwise_token(self):
        """Test main function errors when readwise_token is missing."""
        with patch("sys.argv", ["run"]):
            with patch.dict("os.environ", {}, clear=True):
                with pytest.raises(SystemExit):
                    main()

    def test_main_missing_zotero_key(self):
        """Test main function errors when zotero_key is missing."""
        with patch("sys.argv", ["run", "readwise_token"]):
            with patch.dict("os.environ", {}, clear=True):
                with pytest.raises(SystemExit):
                    main()

    def test_main_missing_zotero_library_id(self):
        """Test main function errors when zotero_library_id is missing."""
        with patch("sys.argv", ["run", "readwise_token", "zotero_key"]):
            with patch.dict("os.environ", {}, clear=True):
                with pytest.raises(SystemExit):
                    main()

    @patch("zotero2readwise.run.Zotero2Readwise")
    @patch("zotero2readwise.run.read_library_version")
    def test_main_invalid_include_annotations(self, mock_read_version, mock_zt2rw):
        """Test main function with invalid --include_annotations value."""
        mock_read_version.return_value = 0

        with patch(
            "sys.argv",
            ["run", "token", "key", "id", "--include_annotations", "invalid"],
        ):
            with pytest.raises(ValueError, match="Invalid value for --include_annotations"):
                main()

    @patch("zotero2readwise.run.Zotero2Readwise")
    @patch("zotero2readwise.run.read_library_version")
    def test_main_default_values(self, mock_read_version, mock_zt2rw):
        """Test main function uses correct default values."""
        mock_instance = Mock()
        mock_zt2rw.return_value = mock_instance
        mock_read_version.return_value = 0

        with patch("sys.argv", ["run", "token", "key", "id"]):
            main()

        call_kwargs = mock_zt2rw.call_args[1]
        assert call_kwargs["include_annotations"] is True
        assert call_kwargs["include_notes"] is False
        assert call_kwargs["filter_colors"] == ()
        assert call_kwargs["filter_tags"] == ()
        assert call_kwargs["include_filter_tags"] is False
        assert call_kwargs["since"] == 0
        assert call_kwargs["write_failures"] is True
        assert call_kwargs["custom_tag"] is None
        assert call_kwargs["zotero_library_type"] == "user"
