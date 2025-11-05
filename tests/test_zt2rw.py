"""Tests for Zotero2Readwise main module."""

from unittest.mock import Mock, patch

import pytest

from zotero2readwise.zotero import ZoteroItem
from zotero2readwise.zt2rw import Zotero2Readwise


class TestZotero2Readwise:
    """Tests for Zotero2Readwise class."""

    @patch("zotero2readwise.zt2rw.get_zotero_client")
    @patch("zotero2readwise.zt2rw.Readwise")
    @patch("zotero2readwise.zt2rw.ZoteroAnnotationsNotes")
    def test_initialization(
        self,
        mock_zan_class,
        mock_rw_class,
        mock_get_client,
        zotero_credentials,
        readwise_token,
    ):
        """Test Zotero2Readwise initialization."""
        mock_client = Mock()
        mock_get_client.return_value = mock_client

        zt_rw = Zotero2Readwise(
            readwise_token=readwise_token,
            zotero_key=zotero_credentials["key"],
            zotero_library_id=zotero_credentials["library_id"],
            zotero_library_type=zotero_credentials["library_type"],
            include_annotations=True,
            include_notes=False,
        )

        mock_get_client.assert_called_once_with(
            library_id=zotero_credentials["library_id"],
            library_type=zotero_credentials["library_type"],
            api_key=zotero_credentials["key"],
        )
        mock_rw_class.assert_called_once_with(readwise_token)
        assert zt_rw.include_annots is True
        assert zt_rw.include_notes is False

    @patch("zotero2readwise.zt2rw.get_zotero_client")
    @patch("zotero2readwise.zt2rw.Readwise")
    @patch("zotero2readwise.zt2rw.ZoteroAnnotationsNotes")
    def test_initialization_with_filters(
        self,
        mock_zan_class,
        mock_rw_class,
        mock_get_client,
        zotero_credentials,
        readwise_token,
    ):
        """Test initialization with color and tag filters."""
        mock_client = Mock()
        mock_get_client.return_value = mock_client

        zt_rw = Zotero2Readwise(
            readwise_token=readwise_token,
            zotero_key=zotero_credentials["key"],
            zotero_library_id=zotero_credentials["library_id"],
            filter_colors=["#ffd400", "#ff6666"],
            filter_tags=["important", "review"],
            include_filter_tags=True,
        )

        # Verify ZoteroAnnotationsNotes was called with correct filters
        call_args = mock_zan_class.call_args
        assert call_args[0][1] == ["#ffd400", "#ff6666"]  # filter_colors
        assert call_args[0][2] == ["important", "review"]  # filter_tags
        assert call_args[0][3] is True  # include_filter_tags

    @patch("zotero2readwise.zt2rw.get_zotero_client")
    @patch("zotero2readwise.zt2rw.Readwise")
    @patch("zotero2readwise.zt2rw.ZoteroAnnotationsNotes")
    def test_get_all_zotero_items_annotations_only(
        self,
        mock_zan_class,
        mock_rw_class,
        mock_get_client,
        zotero_credentials,
        readwise_token,
    ):
        """Test retrieving only annotations."""
        mock_client = Mock()
        mock_get_client.return_value = mock_client

        zt_rw = Zotero2Readwise(
            readwise_token=readwise_token,
            zotero_key=zotero_credentials["key"],
            zotero_library_id=zotero_credentials["library_id"],
            include_annotations=True,
            include_notes=False,
        )

        mock_annotations = [{"key": "ANN1"}, {"key": "ANN2"}]
        mock_client.items.return_value = Mock()
        mock_client.everything.return_value = mock_annotations

        items = zt_rw.get_all_zotero_items()

        assert len(items) == 2
        mock_client.items.assert_called_once_with(itemType="annotation", since=0)

    @patch("zotero2readwise.zt2rw.get_zotero_client")
    @patch("zotero2readwise.zt2rw.Readwise")
    @patch("zotero2readwise.zt2rw.ZoteroAnnotationsNotes")
    def test_get_all_zotero_items_notes_only(
        self,
        mock_zan_class,
        mock_rw_class,
        mock_get_client,
        zotero_credentials,
        readwise_token,
    ):
        """Test retrieving only notes."""
        mock_client = Mock()
        mock_get_client.return_value = mock_client

        zt_rw = Zotero2Readwise(
            readwise_token=readwise_token,
            zotero_key=zotero_credentials["key"],
            zotero_library_id=zotero_credentials["library_id"],
            include_annotations=False,
            include_notes=True,
        )

        mock_notes = [{"key": "NOTE1"}]
        mock_client.items.return_value = Mock()
        mock_client.everything.return_value = mock_notes

        items = zt_rw.get_all_zotero_items()

        assert len(items) == 1
        mock_client.items.assert_called_once_with(itemType="note", since=0)

    @patch("zotero2readwise.zt2rw.get_zotero_client")
    @patch("zotero2readwise.zt2rw.Readwise")
    @patch("zotero2readwise.zt2rw.ZoteroAnnotationsNotes")
    def test_get_all_zotero_items_both(
        self,
        mock_zan_class,
        mock_rw_class,
        mock_get_client,
        zotero_credentials,
        readwise_token,
    ):
        """Test retrieving both annotations and notes."""
        mock_client = Mock()
        mock_get_client.return_value = mock_client

        zt_rw = Zotero2Readwise(
            readwise_token=readwise_token,
            zotero_key=zotero_credentials["key"],
            zotero_library_id=zotero_credentials["library_id"],
            include_annotations=True,
            include_notes=True,
        )

        mock_annotations = [{"key": "ANN1"}, {"key": "ANN2"}]
        mock_notes = [{"key": "NOTE1"}]

        def mock_everything(query):
            # Return different data based on the query type
            if hasattr(query, "itemType"):
                return mock_annotations if query.itemType == "annotation" else mock_notes
            return []

        mock_client.items.return_value = Mock()
        mock_client.everything.side_effect = [mock_annotations, mock_notes]

        items = zt_rw.get_all_zotero_items()

        assert len(items) == 3
        assert mock_client.items.call_count == 2

    @patch("zotero2readwise.zt2rw.get_zotero_client")
    @patch("zotero2readwise.zt2rw.Readwise")
    @patch("zotero2readwise.zt2rw.ZoteroAnnotationsNotes")
    def test_get_all_zotero_items_with_since(
        self,
        mock_zan_class,
        mock_rw_class,
        mock_get_client,
        zotero_credentials,
        readwise_token,
    ):
        """Test retrieving items with 'since' parameter."""
        mock_client = Mock()
        mock_get_client.return_value = mock_client

        zt_rw = Zotero2Readwise(
            readwise_token=readwise_token,
            zotero_key=zotero_credentials["key"],
            zotero_library_id=zotero_credentials["library_id"],
            include_annotations=True,
            include_notes=False,
            since=1234567890,
        )

        mock_client.items.return_value = Mock()
        mock_client.everything.return_value = []

        zt_rw.get_all_zotero_items()

        mock_client.items.assert_called_once_with(itemType="annotation", since=1234567890)

    @patch("zotero2readwise.zt2rw.get_zotero_client")
    @patch("zotero2readwise.zt2rw.Readwise")
    @patch("zotero2readwise.zt2rw.ZoteroAnnotationsNotes")
    def test_retrieve_all_invalid_item_type(
        self,
        mock_zan_class,
        mock_rw_class,
        mock_get_client,
        zotero_credentials,
        readwise_token,
    ):
        """Test that invalid item type raises ValueError."""
        mock_client = Mock()
        mock_get_client.return_value = mock_client

        zt_rw = Zotero2Readwise(
            readwise_token=readwise_token,
            zotero_key=zotero_credentials["key"],
            zotero_library_id=zotero_credentials["library_id"],
        )

        with pytest.raises(ValueError, match="item_type must be either"):
            zt_rw.retrieve_all("invalid_type")

    @patch("zotero2readwise.zt2rw.get_zotero_client")
    @patch("zotero2readwise.zt2rw.Readwise")
    @patch("zotero2readwise.zt2rw.ZoteroAnnotationsNotes")
    def test_run_without_items(
        self,
        mock_zan_class,
        mock_rw_class,
        mock_get_client,
        zotero_credentials,
        readwise_token,
    ):
        """Test running sync without providing items (fetches from Zotero)."""
        mock_client = Mock()
        mock_get_client.return_value = mock_client

        mock_zotero = Mock()
        mock_zan_class.return_value = mock_zotero

        mock_readwise = Mock()
        mock_rw_class.return_value = mock_readwise

        zt_rw = Zotero2Readwise(
            readwise_token=readwise_token,
            zotero_key=zotero_credentials["key"],
            zotero_library_id=zotero_credentials["library_id"],
            include_annotations=True,
            include_notes=False,
        )

        # Mock the retrieval
        mock_items = [{"key": "ITEM1"}]
        mock_client.items.return_value = Mock()
        mock_client.everything.return_value = mock_items

        # Mock formatting
        mock_formatted = [
            ZoteroItem(
                key="ITEM1",
                version=1,
                item_type="annotation",
                text="text",
                annotated_at="2023-01-01",
                annotation_url="https://example.com",
            )
        ]
        mock_zotero.format_items.return_value = mock_formatted
        mock_zotero.failed_items = []

        zt_rw.run()

        mock_zotero.format_items.assert_called_once_with(mock_items)
        mock_readwise.post_zotero_annotations_to_readwise.assert_called_once_with(mock_formatted)

    @patch("zotero2readwise.zt2rw.get_zotero_client")
    @patch("zotero2readwise.zt2rw.Readwise")
    @patch("zotero2readwise.zt2rw.ZoteroAnnotationsNotes")
    def test_run_with_items(
        self,
        mock_zan_class,
        mock_rw_class,
        mock_get_client,
        zotero_credentials,
        readwise_token,
    ):
        """Test running sync with provided items."""
        mock_client = Mock()
        mock_get_client.return_value = mock_client

        mock_zotero = Mock()
        mock_zan_class.return_value = mock_zotero

        mock_readwise = Mock()
        mock_rw_class.return_value = mock_readwise

        zt_rw = Zotero2Readwise(
            readwise_token=readwise_token,
            zotero_key=zotero_credentials["key"],
            zotero_library_id=zotero_credentials["library_id"],
        )

        # Provide items directly
        provided_items = [{"key": "PROVIDED1"}]

        mock_formatted = [
            ZoteroItem(
                key="PROVIDED1",
                version=1,
                item_type="annotation",
                text="text",
                annotated_at="2023-01-01",
                annotation_url="https://example.com",
            )
        ]
        mock_zotero.format_items.return_value = mock_formatted
        mock_zotero.failed_items = []

        zt_rw.run(provided_items)

        mock_zotero.format_items.assert_called_once_with(provided_items)

    @patch("zotero2readwise.zt2rw.get_zotero_client")
    @patch("zotero2readwise.zt2rw.Readwise")
    @patch("zotero2readwise.zt2rw.ZoteroAnnotationsNotes")
    def test_run_with_write_failures_true(
        self,
        mock_zan_class,
        mock_rw_class,
        mock_get_client,
        zotero_credentials,
        readwise_token,
    ):
        """Test that failed items are saved when write_failures=True."""
        mock_client = Mock()
        mock_get_client.return_value = mock_client

        mock_zotero = Mock()
        mock_zan_class.return_value = mock_zotero

        mock_readwise = Mock()
        mock_rw_class.return_value = mock_readwise

        zt_rw = Zotero2Readwise(
            readwise_token=readwise_token,
            zotero_key=zotero_credentials["key"],
            zotero_library_id=zotero_credentials["library_id"],
            write_failures=True,
        )

        provided_items = [{"key": "ITEM1"}]
        mock_zotero.format_items.return_value = []
        mock_zotero.failed_items = [{"key": "FAILED1"}]

        zt_rw.run(provided_items)

        mock_zotero.save_failed_items_to_json.assert_called_once_with("failed_zotero_items.json")

    @patch("zotero2readwise.zt2rw.get_zotero_client")
    @patch("zotero2readwise.zt2rw.Readwise")
    @patch("zotero2readwise.zt2rw.ZoteroAnnotationsNotes")
    def test_run_with_write_failures_false(
        self,
        mock_zan_class,
        mock_rw_class,
        mock_get_client,
        zotero_credentials,
        readwise_token,
    ):
        """Test that failed items are NOT saved when write_failures=False."""
        mock_client = Mock()
        mock_get_client.return_value = mock_client

        mock_zotero = Mock()
        mock_zan_class.return_value = mock_zotero

        mock_readwise = Mock()
        mock_rw_class.return_value = mock_readwise

        zt_rw = Zotero2Readwise(
            readwise_token=readwise_token,
            zotero_key=zotero_credentials["key"],
            zotero_library_id=zotero_credentials["library_id"],
            write_failures=False,
        )

        provided_items = [{"key": "ITEM1"}]
        mock_zotero.format_items.return_value = []
        mock_zotero.failed_items = [{"key": "FAILED1"}]

        zt_rw.run(provided_items)

        mock_zotero.save_failed_items_to_json.assert_not_called()

    @patch("zotero2readwise.zt2rw.get_zotero_client")
    @patch("zotero2readwise.zt2rw.Readwise")
    @patch("zotero2readwise.zt2rw.ZoteroAnnotationsNotes")
    def test_run_with_unicode_items(
        self,
        mock_zan_class,
        mock_rw_class,
        mock_get_client,
        zotero_credentials,
        readwise_token,
    ):
        """Test running sync with Unicode items (issue #90)."""
        mock_client = Mock()
        mock_get_client.return_value = mock_client

        mock_zotero = Mock()
        mock_zan_class.return_value = mock_zotero

        mock_readwise = Mock()
        mock_rw_class.return_value = mock_readwise

        zt_rw = Zotero2Readwise(
            readwise_token=readwise_token,
            zotero_key=zotero_credentials["key"],
            zotero_library_id=zotero_credentials["library_id"],
        )

        # Items with Unicode text
        unicode_items = [
            {
                "key": "UNICODE1",
                "data": {"annotationText": "这是中文文本 技術"},
            }
        ]

        mock_formatted = [
            ZoteroItem(
                key="UNICODE1",
                version=1,
                item_type="annotation",
                text="这是中文文本 技術",
                annotated_at="2023-01-01",
                annotation_url="https://example.com",
            )
        ]
        mock_zotero.format_items.return_value = mock_formatted
        mock_zotero.failed_items = []

        zt_rw.run(unicode_items)

        # Should complete without errors
        mock_readwise.post_zotero_annotations_to_readwise.assert_called_once()
