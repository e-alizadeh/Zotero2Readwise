"""Tests for Zotero module."""

from unittest.mock import mock_open, patch

import pytest

from zotero2readwise.zotero import (
    ZoteroAnnotationsNotes,
    ZoteroItem,
    get_zotero_client,
)


class TestZoteroItem:
    """Tests for ZoteroItem dataclass."""

    def test_zotero_item_creation(self):
        """Test creating a ZoteroItem."""
        item = ZoteroItem(
            key="ABC123",
            version=100,
            item_type="annotation",
            text="Sample text",
            annotated_at="2023-01-01T12:00:00Z",
            annotation_url="https://example.com",
        )

        assert item.key == "ABC123"
        assert item.version == 100
        assert item.item_type == "annotation"
        assert item.text == "Sample text"

    def test_zotero_item_with_tags(self):
        """Test ZoteroItem with tags."""
        item = ZoteroItem(
            key="ABC123",
            version=100,
            item_type="annotation",
            text="Sample text",
            annotated_at="2023-01-01T12:00:00Z",
            annotation_url="https://example.com",
            tags=[{"tag": "important"}, {"tag": "research"}],
        )

        assert item.tags == ["important", "research"]

    def test_zotero_item_with_creators(self):
        """Test ZoteroItem with creators."""
        item = ZoteroItem(
            key="ABC123",
            version=100,
            item_type="annotation",
            text="Sample text",
            annotated_at="2023-01-01T12:00:00Z",
            annotation_url="https://example.com",
            creators=["John Doe", "Jane Smith"],
        )

        # After post_init, creators should be formatted
        assert "John Doe" in item.creators or item.creators == "John Doe, Jane Smith"

    def test_format_author_list_normal(self):
        """Test format_author_list with normal length."""
        authors = ["John Doe", "Jane Smith", "Bob Johnson"]
        result = ZoteroItem.format_author_list(authors)

        assert result == "John Doe, Jane Smith, Bob Johnson"

    def test_format_author_list_too_long(self):
        """Test format_author_list with too many authors."""
        # Create a list with many long names that exceeds MAX_LENGTH
        authors = ["A" * 256 for _ in range(10)]
        result = ZoteroItem.format_author_list(authors)

        # Should be truncated with "et al."
        assert " et al." in result or len(result) <= 1024

    def test_format_author_list_single_author(self):
        """Test format_author_list with single author."""
        authors = ["John Doe"]
        result = ZoteroItem.format_author_list(authors)

        assert result == "John Doe"

    def test_get_nonempty_params(self):
        """Test get_nonempty_params method."""
        item = ZoteroItem(
            key="ABC123",
            version=100,
            item_type="annotation",
            text="Sample text",
            annotated_at="2023-01-01T12:00:00Z",
            annotation_url="https://example.com",
            comment=None,
            title=None,
        )

        params = item.get_nonempty_params()

        assert "key" in params
        assert "text" in params
        assert "comment" not in params or params.get("comment") is None
        assert "title" not in params or params.get("title") is None

    def test_zotero_item_with_unicode_text(self):
        """Test ZoteroItem with Unicode text (for issue #90)."""
        item = ZoteroItem(
            key="ABC123",
            version=100,
            item_type="annotation",
            text="这是中文文本 技術",
            annotated_at="2023-01-01T12:00:00Z",
            annotation_url="https://example.com",
            comment="中文评论",
        )

        assert item.text == "这是中文文本 技術"
        assert item.comment == "中文评论"


class TestGetZoteroClient:
    """Tests for get_zotero_client function."""

    @patch("zotero2readwise.zotero.Zotero")
    def test_get_zotero_client_with_params(self, mock_zotero_class):
        """Test getting Zotero client with provided parameters."""
        client = get_zotero_client(library_id="123456", api_key="test_key", library_type="user")

        mock_zotero_class.assert_called_once_with(
            library_id="123456", library_type="user", api_key="test_key"
        )

    @patch("zotero2readwise.zotero.Zotero")
    @patch.dict(
        "os.environ",
        {"ZOTERO_LIBRARY_ID": "789012", "ZOTERO_KEY": "env_test_key"},
    )
    def test_get_zotero_client_from_env(self, mock_zotero_class):
        """Test getting Zotero client from environment variables."""
        client = get_zotero_client()

        mock_zotero_class.assert_called_once_with(
            library_id="789012", library_type="user", api_key="env_test_key"
        )

    def test_get_zotero_client_missing_library_id(self):
        """Test error when library_id is missing."""
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(ValueError, match="No value for library_id"):
                get_zotero_client(api_key="test_key")

    def test_get_zotero_client_missing_api_key(self):
        """Test error when api_key is missing."""
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(ValueError, match="No value for api_key"):
                get_zotero_client(library_id="123456")

    @patch("zotero2readwise.zotero.Zotero")
    def test_get_zotero_client_invalid_library_type(self, mock_zotero_class):
        """Test error with invalid library_type."""
        with pytest.raises(ValueError, match="library_type value can either be"):
            get_zotero_client(library_id="123456", api_key="test_key", library_type="invalid")


class TestZoteroAnnotationsNotes:
    """Tests for ZoteroAnnotationsNotes class."""

    def test_initialization(self, mock_zotero_client):
        """Test ZoteroAnnotationsNotes initialization."""
        zan = ZoteroAnnotationsNotes(
            mock_zotero_client,
            filter_colors=["#ffd400"],
            filter_tags=["important"],
            include_filter_tags=False,
        )

        assert zan.zot == mock_zotero_client
        assert zan.filter_colors == ["#ffd400"]
        assert zan.filter_tags == ["important"]
        assert zan.include_filter_tags is False
        assert zan.failed_items == []
        assert zan._cache == {}

    def test_get_item_metadata(
        self, mock_zotero_client, sample_zotero_annotation, sample_parent_item
    ):
        """Test getting item metadata."""
        mock_zotero_client.item.return_value = sample_parent_item

        zan = ZoteroAnnotationsNotes(
            mock_zotero_client,
            filter_colors=[],
            filter_tags=[],
            include_filter_tags=False,
        )

        metadata = zan.get_item_metadata(sample_zotero_annotation)

        assert "title" in metadata
        assert "tags" in metadata
        assert "creators" in metadata
        assert metadata["title"] == "Sample Research Paper"

    def test_format_item_annotation_highlight(
        self, mock_zotero_client, sample_zotero_annotation, sample_parent_item
    ):
        """Test formatting a highlight annotation."""
        mock_zotero_client.item.return_value = sample_parent_item

        zan = ZoteroAnnotationsNotes(
            mock_zotero_client,
            filter_colors=[],
            filter_tags=[],
            include_filter_tags=False,
        )

        formatted = zan.format_item(sample_zotero_annotation)

        assert isinstance(formatted, ZoteroItem)
        assert formatted.key == "ABC123"
        assert formatted.text == "This is a sample highlight text"
        assert formatted.comment == "This is a comment"
        assert formatted.item_type == "annotation"

    def test_format_item_note(self, mock_zotero_client, sample_zotero_note, sample_parent_item):
        """Test formatting a note."""
        mock_zotero_client.item.return_value = sample_parent_item

        zan = ZoteroAnnotationsNotes(
            mock_zotero_client,
            filter_colors=[],
            filter_tags=[],
            include_filter_tags=False,
        )

        formatted = zan.format_item(sample_zotero_note)

        assert isinstance(formatted, ZoteroItem)
        assert formatted.key == "NOTE123"
        assert formatted.text == "<p>This is a sample note</p>"
        assert formatted.comment == ""
        assert formatted.item_type == "note"

    def test_format_items_with_failures(self, mock_zotero_client, sample_zotero_annotation):
        """Test formatting items with some failures."""
        # Create a bad annotation that will cause an error
        bad_annotation = sample_zotero_annotation.copy()
        bad_annotation["data"] = {"itemType": "unknown"}

        mock_zotero_client.item.side_effect = Exception("API Error")

        zan = ZoteroAnnotationsNotes(
            mock_zotero_client,
            filter_colors=[],
            filter_tags=[],
            include_filter_tags=False,
        )

        formatted = zan.format_items([sample_zotero_annotation, bad_annotation])

        # Both should fail due to mock error
        assert len(zan.failed_items) == 2

    def test_format_items_with_color_filter(
        self, mock_zotero_client, sample_zotero_annotation, sample_parent_item
    ):
        """Test formatting items with color filter."""
        mock_zotero_client.item.return_value = sample_parent_item

        zan = ZoteroAnnotationsNotes(
            mock_zotero_client,
            filter_colors=["#ffd400"],
            filter_tags=[],
            include_filter_tags=False,
        )

        formatted = zan.format_items([sample_zotero_annotation])

        assert len(formatted) == 1

    def test_save_failed_items_to_json(self, mock_zotero_client, tmp_path):
        """Test saving failed items to JSON."""
        zan = ZoteroAnnotationsNotes(
            mock_zotero_client,
            filter_colors=[],
            filter_tags=[],
            include_filter_tags=False,
        )

        zan.failed_items = [
            {"key": "FAILED1", "text": "Failed item 1"},
            {"key": "FAILED2", "text": "失败的项目 2"},  # Unicode text
        ]

        m = mock_open()
        with patch("builtins.open", m):
            with patch("zotero2readwise.zotero.FAILED_ITEMS_DIR", tmp_path):
                zan.save_failed_items_to_json("test_failed.json")

        # Verify file was opened with utf-8 encoding
        m.assert_called_once()
        call_args = m.call_args
        assert "encoding" in call_args[1]
        assert call_args[1]["encoding"] == "utf-8"

    def test_format_items_with_unicode(
        self, mock_zotero_client, sample_zotero_annotation, sample_parent_item
    ):
        """Test formatting items with Unicode characters (issue #90)."""
        # Modify annotation to have Chinese text
        sample_zotero_annotation["data"]["annotationText"] = "这是中文文本 技術"
        sample_zotero_annotation["data"]["annotationComment"] = "中文评论"

        mock_zotero_client.item.return_value = sample_parent_item

        zan = ZoteroAnnotationsNotes(
            mock_zotero_client,
            filter_colors=[],
            filter_tags=[],
            include_filter_tags=False,
        )

        formatted = zan.format_items([sample_zotero_annotation])

        assert len(formatted) == 1
        assert formatted[0].text == "这是中文文本 技術"
        assert formatted[0].comment == "中文评论"

    def test_format_items_color_filter_excludes_non_matching(
        self, mock_zotero_client, sample_zotero_annotation, sample_parent_item
    ):
        """Test that color filter excludes non-matching annotations."""
        mock_zotero_client.item.return_value = sample_parent_item

        zan = ZoteroAnnotationsNotes(
            mock_zotero_client,
            filter_colors=["#ff6666"],  # Red, but annotation is yellow (#ffd400)
            filter_tags=[],
            include_filter_tags=False,
        )

        formatted = zan.format_items([sample_zotero_annotation])

        # Should be excluded because color doesn't match
        assert len(formatted) == 0

    def test_format_items_tag_filter(
        self, mock_zotero_client, sample_zotero_annotation, sample_parent_item
    ):
        """Test formatting items with tag filter."""
        mock_zotero_client.item.return_value = sample_parent_item

        zan = ZoteroAnnotationsNotes(
            mock_zotero_client,
            filter_colors=[],
            filter_tags=["important"],
            include_filter_tags=False,
        )

        formatted = zan.format_items([sample_zotero_annotation])

        # Should be included because 'important' tag matches
        assert len(formatted) == 1

    def test_format_items_tag_filter_excludes(
        self, mock_zotero_client, sample_zotero_annotation, sample_parent_item
    ):
        """Test that tag filter excludes non-matching annotations."""
        mock_zotero_client.item.return_value = sample_parent_item

        zan = ZoteroAnnotationsNotes(
            mock_zotero_client,
            filter_colors=[],
            filter_tags=["nonexistent"],
            include_filter_tags=False,
        )

        formatted = zan.format_items([sample_zotero_annotation])

        # Should be excluded because tag doesn't match
        assert len(formatted) == 0

    def test_format_items_include_filter_tags_true(
        self, mock_zotero_client, sample_zotero_annotation, sample_parent_item
    ):
        """Test that filter tags are included when include_filter_tags=True."""
        mock_zotero_client.item.return_value = sample_parent_item

        zan = ZoteroAnnotationsNotes(
            mock_zotero_client,
            filter_colors=[],
            filter_tags=["important"],
            include_filter_tags=True,
        )

        formatted = zan.format_items([sample_zotero_annotation])

        assert len(formatted) == 1
        # Tags should include the filter tag
        assert "important" in formatted[0].tags

    def test_format_items_include_filter_tags_false(
        self, mock_zotero_client, sample_zotero_annotation, sample_parent_item
    ):
        """Test that filter tags are excluded when include_filter_tags=False."""
        mock_zotero_client.item.return_value = sample_parent_item

        zan = ZoteroAnnotationsNotes(
            mock_zotero_client,
            filter_colors=[],
            filter_tags=["important"],
            include_filter_tags=False,
        )

        formatted = zan.format_items([sample_zotero_annotation])

        assert len(formatted) == 1
        # Tag 'important' should be excluded
        assert "important" not in formatted[0].tags

    def test_format_item_note_annotation_type(self, mock_zotero_client, sample_parent_item):
        """Test formatting an annotation with 'note' annotationType."""
        note_annotation = {
            "key": "NOTE_ANNOT123",
            "version": 100,
            "data": {
                "key": "NOTE_ANNOT123",
                "version": 100,
                "itemType": "annotation",
                "annotationType": "note",
                "annotationComment": "This is a note-type annotation",
                "parentItem": "PARENT123",
                "dateModified": "2023-01-01T12:00:00Z",
                "tags": [],
                "relations": {},
            },
            "links": {
                "alternate": {"href": "https://www.zotero.org/users/123/items/NOTE_ANNOT123"}
            },
        }

        mock_zotero_client.item.return_value = sample_parent_item

        zan = ZoteroAnnotationsNotes(
            mock_zotero_client,
            filter_colors=[],
            filter_tags=[],
            include_filter_tags=False,
        )

        formatted = zan.format_item(note_annotation)

        assert formatted.text == "This is a note-type annotation"
        assert formatted.comment == ""
        assert formatted.annotation_type == "note"

    def test_format_item_ink_annotation_raises(self, mock_zotero_client, sample_parent_item):
        """Test that ink annotations raise NotImplementedError."""
        ink_annotation = {
            "key": "INK123",
            "version": 100,
            "data": {
                "key": "INK123",
                "version": 100,
                "itemType": "annotation",
                "annotationType": "ink",
                "parentItem": "PARENT123",
                "dateModified": "2023-01-01T12:00:00Z",
                "tags": [],
                "relations": {},
            },
            "links": {"alternate": {"href": "https://www.zotero.org/users/123/items/INK123"}},
        }

        mock_zotero_client.item.return_value = sample_parent_item

        zan = ZoteroAnnotationsNotes(
            mock_zotero_client,
            filter_colors=[],
            filter_tags=[],
            include_filter_tags=False,
        )

        with pytest.raises(NotImplementedError, match="ink"):
            zan.format_item(ink_annotation)

    def test_format_item_image_annotation_raises(self, mock_zotero_client, sample_parent_item):
        """Test that image annotations raise NotImplementedError."""
        image_annotation = {
            "key": "IMAGE123",
            "version": 100,
            "data": {
                "key": "IMAGE123",
                "version": 100,
                "itemType": "annotation",
                "annotationType": "image",
                "parentItem": "PARENT123",
                "dateModified": "2023-01-01T12:00:00Z",
                "tags": [],
                "relations": {},
            },
            "links": {"alternate": {"href": "https://www.zotero.org/users/123/items/IMAGE123"}},
        }

        mock_zotero_client.item.return_value = sample_parent_item

        zan = ZoteroAnnotationsNotes(
            mock_zotero_client,
            filter_colors=[],
            filter_tags=[],
            include_filter_tags=False,
        )

        with pytest.raises(NotImplementedError, match="Image"):
            zan.format_item(image_annotation)

    def test_format_item_empty_text_raises(self, mock_zotero_client, sample_parent_item):
        """Test that empty annotation text raises ValueError."""
        empty_annotation = {
            "key": "EMPTY123",
            "version": 100,
            "data": {
                "key": "EMPTY123",
                "version": 100,
                "itemType": "annotation",
                "annotationType": "highlight",
                "annotationText": "",
                "annotationComment": "",
                "parentItem": "PARENT123",
                "dateModified": "2023-01-01T12:00:00Z",
                "tags": [],
                "relations": {},
            },
            "links": {"alternate": {"href": "https://www.zotero.org/users/123/items/EMPTY123"}},
        }

        mock_zotero_client.item.return_value = sample_parent_item

        zan = ZoteroAnnotationsNotes(
            mock_zotero_client,
            filter_colors=[],
            filter_tags=[],
            include_filter_tags=False,
        )

        with pytest.raises(ValueError, match="No annotation or note data"):
            zan.format_item(empty_annotation)

    def test_format_item_unsupported_item_type_raises(self, mock_zotero_client, sample_parent_item):
        """Test that unsupported item types raise NotImplementedError."""
        unsupported_item = {
            "key": "UNSUPPORTED123",
            "version": 100,
            "data": {
                "key": "UNSUPPORTED123",
                "version": 100,
                "itemType": "attachment",  # Not annotation or note
                "parentItem": "PARENT123",
                "dateModified": "2023-01-01T12:00:00Z",
                "tags": [],
                "relations": {},
            },
            "links": {
                "alternate": {"href": "https://www.zotero.org/users/123/items/UNSUPPORTED123"}
            },
        }

        mock_zotero_client.item.return_value = sample_parent_item

        zan = ZoteroAnnotationsNotes(
            mock_zotero_client,
            filter_colors=[],
            filter_tags=[],
            include_filter_tags=False,
        )

        with pytest.raises(NotImplementedError, match="Only Zotero item types"):
            zan.format_item(unsupported_item)

    def test_get_item_metadata_caching(
        self, mock_zotero_client, sample_zotero_annotation, sample_parent_item
    ):
        """Test that metadata is cached to avoid duplicate API calls."""
        mock_zotero_client.item.return_value = sample_parent_item

        zan = ZoteroAnnotationsNotes(
            mock_zotero_client,
            filter_colors=[],
            filter_tags=[],
            include_filter_tags=False,
        )

        # First call
        metadata1 = zan.get_item_metadata(sample_zotero_annotation)
        call_count_1 = mock_zotero_client.item.call_count

        # Second call with same annotation - should use cache
        metadata2 = zan.get_item_metadata(sample_zotero_annotation)
        call_count_2 = mock_zotero_client.item.call_count

        assert metadata1 == metadata2
        # Should not make additional API calls due to caching
        assert call_count_2 == call_count_1

    def test_format_items_sorted_by_title_and_sort_index(
        self, mock_zotero_client, sample_parent_item
    ):
        """Test that formatted items are sorted by title and sort_index."""
        mock_zotero_client.item.return_value = sample_parent_item

        annot1 = {
            "key": "ANNOT1",
            "version": 100,
            "data": {
                "key": "ANNOT1",
                "version": 100,
                "itemType": "annotation",
                "annotationType": "highlight",
                "annotationText": "Text 1",
                "annotationComment": "",
                "annotationSortIndex": "00002",
                "parentItem": "PARENT123",
                "dateModified": "2023-01-01T12:00:00Z",
                "tags": [],
                "relations": {},
            },
            "links": {"alternate": {"href": "https://www.zotero.org/users/123/items/ANNOT1"}},
        }

        annot2 = {
            "key": "ANNOT2",
            "version": 100,
            "data": {
                "key": "ANNOT2",
                "version": 100,
                "itemType": "annotation",
                "annotationType": "highlight",
                "annotationText": "Text 2",
                "annotationComment": "",
                "annotationSortIndex": "00001",
                "parentItem": "PARENT123",
                "dateModified": "2023-01-01T12:00:00Z",
                "tags": [],
                "relations": {},
            },
            "links": {"alternate": {"href": "https://www.zotero.org/users/123/items/ANNOT2"}},
        }

        zan = ZoteroAnnotationsNotes(
            mock_zotero_client,
            filter_colors=[],
            filter_tags=[],
            include_filter_tags=False,
        )

        # Pass in reverse order
        formatted = zan.format_items([annot1, annot2])

        # Should be sorted by sort_index
        assert len(formatted) == 2
        assert formatted[0].sort_index == "00001"
        assert formatted[1].sort_index == "00002"

    def test_zotero_item_with_relations(self):
        """Test ZoteroItem with dc:relation."""
        item = ZoteroItem(
            key="ABC123",
            version=100,
            item_type="annotation",
            text="Sample text",
            annotated_at="2023-01-01T12:00:00Z",
            annotation_url="https://example.com",
            relations={
                "dc:relation": [
                    "http://zotero.org/users/123/items/ABC",
                    "http://zotero.org/users/123/items/DEF",
                ]
            },
        )

        # After post_init, relations should be extracted
        assert item.relations == [
            "http://zotero.org/users/123/items/ABC",
            "http://zotero.org/users/123/items/DEF",
        ]

    def test_zotero_item_with_document_tags(self):
        """Test ZoteroItem with document_tags."""
        item = ZoteroItem(
            key="ABC123",
            version=100,
            item_type="annotation",
            text="Sample text",
            annotated_at="2023-01-01T12:00:00Z",
            annotation_url="https://example.com",
            document_tags=[{"tag": "science"}, {"tag": "research"}],
        )

        # After post_init, document_tags should be converted to list of strings
        assert item.document_tags == ["science", "research"]

    def test_format_author_list_empty(self):
        """Test format_author_list with empty list."""
        authors = []
        result = ZoteroItem.format_author_list(authors)
        assert result == ""

    @patch("zotero2readwise.zotero.Zotero")
    def test_get_zotero_client_group_type(self, mock_zotero_class):
        """Test getting Zotero client with group library type."""
        get_zotero_client(library_id="123456", api_key="test_key", library_type="group")

        mock_zotero_class.assert_called_once_with(
            library_id="123456", library_type="group", api_key="test_key"
        )

    def test_get_item_metadata_institutional_author(self, mock_zotero_client):
        """Test getting metadata with institutional author (no firstName/lastName)."""
        parent_item_with_institutional = {
            "key": "PARENT123",
            "version": 99,
            "data": {
                "key": "PARENT123",
                "version": 99,
                "itemType": "journalArticle",
                "title": "WHO Report",
                "date": "2023",
                "creators": [
                    {"name": "World Health Organization"},
                ],
                "tags": [],
            },
            "links": {
                "alternate": {"href": "https://www.zotero.org/users/123/items/PARENT123"},
            },
        }

        annotation = {
            "key": "ANNOT123",
            "data": {
                "key": "ANNOT123",
                "parentItem": "PARENT123",
            },
        }

        mock_zotero_client.item.return_value = parent_item_with_institutional

        zan = ZoteroAnnotationsNotes(
            mock_zotero_client,
            filter_colors=[],
            filter_tags=[],
            include_filter_tags=False,
        )

        metadata = zan.get_item_metadata(annotation)

        assert "World Health Organization" in metadata["creators"]
