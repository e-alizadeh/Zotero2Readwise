"""Tests for Readwise module."""

from unittest.mock import Mock, mock_open, patch

import pytest

from zotero2readwise.exception import Zotero2ReadwiseError
from zotero2readwise.readwise import (
    Category,
    Readwise,
    ReadwiseAPI,
    ReadwiseHighlight,
)
from zotero2readwise.zotero import ZoteroItem


class TestReadwiseAPI:
    """Tests for ReadwiseAPI dataclass."""

    def test_readwise_api_endpoints(self):
        """Test ReadwiseAPI endpoints."""
        api = ReadwiseAPI()

        assert api.base_url == "https://readwise.io/api/v2"
        assert api.highlights == "https://readwise.io/api/v2/highlights/"
        assert api.books == "https://readwise.io/api/v2/books/"


class TestCategory:
    """Tests for Category enum."""

    def test_category_values(self):
        """Test Category enum values."""
        assert Category.articles.value == 1
        assert Category.books.value == 2
        assert Category.tweets.value == 3
        assert Category.podcasts.value == 4

    def test_category_names(self):
        """Test Category enum names."""
        assert Category.articles.name == "articles"
        assert Category.books.name == "books"


class TestReadwiseHighlight:
    """Tests for ReadwiseHighlight dataclass."""

    def test_readwise_highlight_creation(self):
        """Test creating a ReadwiseHighlight."""
        highlight = ReadwiseHighlight(
            text="Sample highlight text",
            title="Sample Book",
            author="John Doe",
            category="books",
        )

        assert highlight.text == "Sample highlight text"
        assert highlight.title == "Sample Book"
        assert highlight.author == "John Doe"
        assert highlight.category == "books"

    def test_readwise_highlight_location_zero(self):
        """Test that location 0 becomes None."""
        highlight = ReadwiseHighlight(text="Sample text", location=0)

        assert highlight.location is None

    def test_readwise_highlight_location_valid(self):
        """Test that valid location is preserved."""
        highlight = ReadwiseHighlight(text="Sample text", location=42)

        assert highlight.location == 42

    def test_get_nonempty_params(self):
        """Test get_nonempty_params method."""
        highlight = ReadwiseHighlight(
            text="Sample text",
            title="Title",
            author=None,
            note="A note",
        )

        params = highlight.get_nonempty_params()

        assert "text" in params
        assert "title" in params
        assert "note" in params
        assert "author" not in params or params.get("author") is None

    def test_readwise_highlight_with_unicode(self):
        """Test ReadwiseHighlight with Unicode text."""
        highlight = ReadwiseHighlight(
            text="这是中文文本",
            title="中文书籍",
            author="张三",
            note="中文笔记",
        )

        assert highlight.text == "这是中文文本"
        assert highlight.title == "中文书籍"
        assert highlight.author == "张三"
        assert highlight.note == "中文笔记"


class TestReadwise:
    """Tests for Readwise class."""

    def test_initialization(self, readwise_token):
        """Test Readwise initialization."""
        rw = Readwise(readwise_token)

        assert rw._token == readwise_token
        assert rw._header == {"Authorization": f"Token {readwise_token}"}
        assert rw.failed_highlights == []

    @patch("zotero2readwise.readwise.requests.post")
    def test_create_highlights_success(self, mock_post, readwise_token):
        """Test successful highlight creation."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        rw = Readwise(readwise_token)
        highlights = [{"text": "Sample highlight", "title": "Sample Book"}]

        rw.create_highlights(highlights)

        mock_post.assert_called_once()
        call_args = mock_post.call_args
        assert call_args[1]["json"] == {"highlights": highlights}

    @patch("zotero2readwise.readwise.requests.post")
    def test_create_highlights_failure(self, mock_post, readwise_token):
        """Test failed highlight creation."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.reason = "Bad Request"
        mock_response.json.return_value = {"error": "Invalid data"}
        mock_post.return_value = mock_response

        rw = Readwise(readwise_token)
        highlights = [{"text": "Sample highlight"}]

        m = mock_open()
        with patch("builtins.open", m):
            with pytest.raises(Zotero2ReadwiseError, match="Uploading to Readwise failed"):
                rw.create_highlights(highlights)

    def test_convert_tags_to_readwise_format(self, readwise_token):
        """Test converting tags to Readwise format."""
        rw = Readwise(readwise_token)

        tags = ["Machine Learning", "AI", "Deep Learning"]
        result = rw.convert_tags_to_readwise_format(tags)

        assert ".machine_learning" in result
        assert ".ai" in result
        assert ".deep_learning" in result

    def test_convert_tags_empty_list(self, readwise_token):
        """Test converting empty tag list."""
        rw = Readwise(readwise_token)

        result = rw.convert_tags_to_readwise_format([])

        assert result == ""

    def test_format_readwise_note_with_tags_and_comment(self, readwise_token):
        """Test formatting note with tags and comment."""
        rw = Readwise(readwise_token)

        tags = ["important", "research"]
        comment = "This is a great insight"

        result = rw.format_readwise_note(tags, comment)

        assert ".important" in result
        assert ".research" in result
        assert "This is a great insight" in result

    def test_format_readwise_note_tags_only(self, readwise_token):
        """Test formatting note with only tags."""
        rw = Readwise(readwise_token)

        tags = ["tag1"]
        result = rw.format_readwise_note(tags, None)

        assert ".tag1" in result

    def test_format_readwise_note_comment_only(self, readwise_token):
        """Test formatting note with only comment."""
        rw = Readwise(readwise_token)

        result = rw.format_readwise_note([], "Just a comment")

        assert result == "Just a comment"

    def test_format_readwise_note_empty(self, readwise_token):
        """Test formatting note with no tags or comment."""
        rw = Readwise(readwise_token)

        result = rw.format_readwise_note([], None)

        assert result is None

    def test_convert_zotero_annotation_to_readwise_highlight(self, readwise_token):
        """Test converting Zotero annotation to Readwise highlight."""
        rw = Readwise(readwise_token)

        zotero_item = ZoteroItem(
            key="ABC123",
            version=100,
            item_type="annotation",
            text="Sample highlight",
            annotated_at="2023-01-01T12:00:00Z",
            annotation_url="https://www.zotero.org/users/123/items/ABC123",
            comment="My comment",
            title="Sample Paper",
            tags=[{"tag": "important"}],
            document_type="journalArticle",
            creators=["John Doe"],
            source_url="https://example.com/paper",
            page_label="10",
            attachment_url="https://www.zotero.org/users/123/items/ATTACH123",
        )

        highlight = rw.convert_zotero_annotation_to_readwise_highlight(zotero_item)

        assert isinstance(highlight, ReadwiseHighlight)
        assert highlight.text == "Sample highlight"
        assert highlight.title == "Sample Paper"
        # After format_author_list, the list is joined
        assert "John Doe" in highlight.author or highlight.author == "John Doe"
        assert highlight.location == 10
        assert highlight.category == Category.articles.name

    def test_convert_zotero_annotation_book_category(self, readwise_token):
        """Test that books are categorized correctly."""
        rw = Readwise(readwise_token)

        zotero_item = ZoteroItem(
            key="ABC123",
            version=100,
            item_type="annotation",
            text="Sample highlight",
            annotated_at="2023-01-01T12:00:00Z",
            annotation_url="https://www.zotero.org/users/123/items/ABC123",
            title="Sample Book",
            tags=[],
            document_type="book",
            creators="Jane Smith",
            source_url="https://example.com/book",
        )

        highlight = rw.convert_zotero_annotation_to_readwise_highlight(zotero_item)

        assert highlight.category == Category.books.name

    def test_convert_zotero_annotation_with_zotero_url(self, readwise_token):
        """Test Zotero PDF URL generation."""
        rw = Readwise(readwise_token)

        zotero_item = ZoteroItem(
            key="ABC123",
            version=100,
            item_type="annotation",
            text="Sample highlight",
            annotated_at="2023-01-01T12:00:00Z",
            annotation_url="https://www.zotero.org/users/123/items/ABC123",
            title="Sample Paper",
            tags=[],
            document_type="journalArticle",
            source_url="https://example.com/paper",
            page_label="5",
            attachment_url="https://www.zotero.org/users/123/items/ATTACH456",
        )

        highlight = rw.convert_zotero_annotation_to_readwise_highlight(zotero_item)

        assert "zotero://open-pdf/library/items/ATTACH456" in highlight.highlight_url
        assert "page=5" in highlight.highlight_url
        assert "annotation=ABC123" in highlight.highlight_url

    @patch("zotero2readwise.readwise.requests.post")
    def test_post_zotero_annotations_to_readwise_success(self, mock_post, readwise_token):
        """Test posting annotations to Readwise."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        rw = Readwise(readwise_token)

        annotations = [
            ZoteroItem(
                key="ABC123",
                version=100,
                item_type="annotation",
                text="Sample highlight",
                annotated_at="2023-01-01T12:00:00Z",
                annotation_url="https://www.zotero.org/users/123/items/ABC123",
                title="Sample Paper",
                tags=[],
                document_type="journalArticle",
                source_url="https://example.com",
            )
        ]

        rw.post_zotero_annotations_to_readwise(annotations)

        mock_post.assert_called_once()
        assert len(rw.failed_highlights) == 0

    def test_post_zotero_annotations_text_too_long(self, readwise_token):
        """Test handling of annotations with text that's too long."""
        rw = Readwise(readwise_token)

        # Create annotation with text exceeding 8191 characters
        long_text = "A" * 8200

        annotations = [
            ZoteroItem(
                key="ABC123",
                version=100,
                item_type="annotation",
                text=long_text,
                annotated_at="2023-01-01T12:00:00Z",
                annotation_url="https://www.zotero.org/users/123/items/ABC123",
                title="Sample Paper",
                tags=[],
                document_type="journalArticle",
                source_url="https://example.com",
            )
        ]

        with patch("zotero2readwise.readwise.requests.post") as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_post.return_value = mock_response

            rw.post_zotero_annotations_to_readwise(annotations)

        # The long annotation should be in failed_highlights
        assert len(rw.failed_highlights) == 1

    def test_save_failed_items_to_json(self, readwise_token, tmp_path):
        """Test saving failed highlights to JSON."""
        rw = Readwise(readwise_token)

        rw.failed_highlights = [
            {"key": "FAILED1", "text": "Failed highlight 1"},
            {"key": "FAILED2", "text": "失败的高亮 2"},  # Unicode text
        ]

        m = mock_open()
        with patch("builtins.open", m):
            with patch("zotero2readwise.readwise.FAILED_ITEMS_DIR", tmp_path):
                rw.save_failed_items_to_json("test_failed.json")

        # Verify file was opened with utf-8 encoding and ensure_ascii=False
        m.assert_called_once()
        call_args = m.call_args
        assert "encoding" in call_args[1]
        assert call_args[1]["encoding"] == "utf-8"

    def test_convert_zotero_annotation_with_unicode(self, readwise_token):
        """Test converting Zotero annotation with Unicode to Readwise (issue #90)."""
        rw = Readwise(readwise_token)

        zotero_item = ZoteroItem(
            key="ABC123",
            version=100,
            item_type="annotation",
            text="这是中文文本 技術",
            annotated_at="2023-01-01T12:00:00Z",
            annotation_url="https://www.zotero.org/users/123/items/ABC123",
            comment="中文评论",
            title="中文论文",
            tags=[{"tag": "机器学习"}],
            document_type="journalArticle",
            creators=["张三"],
            source_url="https://example.com",
        )

        highlight = rw.convert_zotero_annotation_to_readwise_highlight(zotero_item)

        assert highlight.text == "这是中文文本 技術"
        assert highlight.title == "中文论文"
        # After format_author_list, the list is joined
        assert "张三" in highlight.author or highlight.author == "张三"
        assert ".机器学习" in highlight.note
        assert "中文评论" in highlight.note
