"""Readwise API interaction module.

This module provides classes for interacting with the Readwise API
to upload highlights from Zotero annotations.

Classes:
    ReadwiseAPI: Dataclass containing Readwise API endpoint URLs.
    Category: Enum for Readwise highlight categories.
    ReadwiseHighlight: Dataclass representing a Readwise highlight.
    Readwise: Main client class for Readwise API operations.
"""

from dataclasses import dataclass
from enum import Enum
from json import dump

import requests

from zotero2readwise import FAILED_ITEMS_DIR
from zotero2readwise.exception import Zotero2ReadwiseError
from zotero2readwise.helper import sanitize_tag
from zotero2readwise.zotero import ZoteroItem


@dataclass
class ReadwiseAPI:
    """Dataclass containing Readwise API v2 endpoint URLs.

    Attributes:
        base_url: Base URL for Readwise API v2.
        highlights: Endpoint for highlight operations.
        books: Endpoint for book operations.
    """

    base_url: str = "https://readwise.io/api/v2"
    highlights: str = base_url + "/highlights/"
    books: str = base_url + "/books/"


class Category(Enum):
    """Enum representing Readwise highlight categories.

    Values:
        articles: Category for article highlights (value: 1).
        books: Category for book highlights (value: 2).
        tweets: Category for tweet highlights (value: 3).
        podcasts: Category for podcast highlights (value: 4).
    """

    articles = 1
    books = 2
    tweets = 3
    podcasts = 4


@dataclass
class ReadwiseHighlight:
    """Dataclass representing a Readwise highlight.

    This class maps to the Readwise API highlight format and is used
    as an intermediate representation before uploading to Readwise.

    Attributes:
        text: The highlighted text content (required).
        title: Title of the source document.
        author: Author(s) of the source document.
        image_url: URL to an image for the source.
        source_url: URL to the original source.
        source_type: Type of the source (e.g., "zotero").
        category: Category name ("articles", "books", "tweets", "podcasts").
        note: Note/comment attached to the highlight (includes tags).
        location: Page number or position in the document.
        location_type: Type of location (default: "page").
        highlighted_at: ISO timestamp when the highlight was created.
        highlight_url: Deep link to the highlight in the source app.
    """

    text: str
    title: str | None = None
    author: str | None = None
    image_url: str | None = None
    source_url: str | None = None
    source_type: str | None = None
    category: str | None = None
    note: str | None = None
    location: int | None = 0
    location_type: str | None = "page"
    highlighted_at: str | None = None
    highlight_url: str | None = None

    def __post_init__(self):
        """Post-initialization to normalize location value."""
        if not self.location:
            self.location = None

    def get_nonempty_params(self) -> dict:
        """Return a dictionary of non-empty/non-None attributes.

        Returns:
            Dictionary containing only attributes with truthy values,
            suitable for JSON serialization to Readwise API.
        """
        return {k: v for k, v in self.__dict__.items() if v}


class Readwise:
    """Client class for Readwise API operations.

    Handles authentication, formatting, and uploading of highlights
    to the Readwise service.

    Attributes:
        endpoints: ReadwiseAPI instance with endpoint URLs.
        failed_highlights: List of highlights that failed to upload.
        custom_tag: Optional custom tag to add to all highlights.

    Example:
        >>> rw = Readwise("your_token")
        >>> rw.create_highlights([{"text": "Sample highlight", "title": "Book"}])
    """

    def __init__(self, readwise_token: str, custom_tag: str | None = None):
        """Initialize the Readwise client.

        Args:
            readwise_token: Readwise API access token.
            custom_tag: Optional tag to add to all uploaded highlights.
        """
        self._token = readwise_token
        self._header = {"Authorization": f"Token {self._token}"}
        self.endpoints = ReadwiseAPI
        self.failed_highlights: list = []
        self.custom_tag = custom_tag

    def create_highlights(self, highlights: list[dict]) -> None:
        """Upload highlights to Readwise API.

        Args:
            highlights: List of highlight dictionaries to upload.

        Raises:
            Zotero2ReadwiseError: If the API request fails (non-200 status).
        """
        resp = requests.post(
            url=self.endpoints.highlights,
            headers=self._header,
            json={"highlights": highlights},
        )
        if resp.status_code != 200:
            error_log_file = f"error_log_{resp.status_code}_failed_post_request_to_readwise.json"
            # Handle empty or invalid JSON responses gracefully
            try:
                error_content = (
                    resp.json() if resp.text.strip() else {"error": "Empty response body"}
                )
            except ValueError:
                error_content = {
                    "error": "Invalid JSON response",
                    "raw_response": resp.text[:500],
                }
            with open(error_log_file, "w", encoding="utf-8") as f:
                dump(error_content, f, indent=4, ensure_ascii=False)
            raise Zotero2ReadwiseError(
                f"Uploading to Readwise failed with following details:\n"
                f"POST request Status Code={resp.status_code} ({resp.reason})\n"
                f"Error log is saved to {error_log_file} file."
            )

    @staticmethod
    def convert_tags_to_readwise_format(tags: list[str] | None) -> str:
        """Convert tags to Readwise's inline tag format.

        Args:
            tags: List of tag strings, or None.

        Returns:
            Space-separated string of tags in Readwise format (e.g., ".tag1 .tag2"),
            or empty string if tags is None or empty.
        """
        if not tags:
            return ""
        return " ".join([f".{sanitize_tag(t.lower())}" for t in tags])

    def format_readwise_note(self, tags: list[str] | None, comment: str | None) -> str | None:
        """Format tags and comment into a Readwise note string.

        Combines custom tag, annotation tags, and comment into the format
        expected by Readwise's note field.

        Args:
            tags: List of tag strings from the annotation.
            comment: Optional comment text.

        Returns:
            Formatted note string, or None if no content.
        """
        rw_tags = self.convert_tags_to_readwise_format(tags)
        highlight_note = ""
        # Add custom tag first if specified
        if self.custom_tag:
            highlight_note += f".{sanitize_tag(self.custom_tag.lower())} "
        if rw_tags:
            highlight_note += rw_tags + "\n"
        elif self.custom_tag:
            # Add newline after custom tag if no other tags
            highlight_note = highlight_note.rstrip() + "\n"
        if comment:
            highlight_note += comment
        return highlight_note if highlight_note else None

    def convert_zotero_annotation_to_readwise_highlight(
        self, annot: ZoteroItem
    ) -> ReadwiseHighlight:
        """Convert a ZoteroItem to a ReadwiseHighlight.

        Args:
            annot: ZoteroItem instance to convert.

        Returns:
            ReadwiseHighlight instance ready for upload.
        """
        highlight_note = self.format_readwise_note(tags=annot.tags, comment=annot.comment)
        if annot.page_label and annot.page_label.isnumeric():
            location = int(annot.page_label)
        else:
            location = 0
        highlight_url = None
        if annot.attachment_url is not None:
            attachment_id = annot.attachment_url.split("/")[-1]
            annot_id = annot.annotation_url.split("/")[-1]
            highlight_url = f"zotero://open-pdf/library/items/{attachment_id}?page={location}%&annotation={annot_id}"
        return ReadwiseHighlight(
            text=annot.text,
            title=annot.title,
            note=highlight_note,
            author=annot.creators,
            category=(
                Category.articles.name if annot.document_type != "book" else Category.books.name
            ),
            highlighted_at=annot.annotated_at,
            source_url=annot.source_url,
            highlight_url=(annot.annotation_url if highlight_url is None else highlight_url),
            location=location,
        )

    def post_zotero_annotations_to_readwise(self, zotero_annotations: list[ZoteroItem]) -> None:
        """Upload Zotero annotations to Readwise.

        Converts each ZoteroItem to a ReadwiseHighlight and uploads them
        in batch. Handles errors gracefully, storing failed items.

        Args:
            zotero_annotations: List of ZoteroItem instances to upload.

        Note:
            Annotations with text exceeding 8191 characters are skipped
            and added to failed_highlights.
        """
        print(
            f"\nReadwise: Push {len(zotero_annotations)} Zotero annotations/notes to Readwise...\n"
            f"It may take some time depending on the number of highlights...\n"
            f"A complete message will show up once it's done!\n"
        )
        rw_highlights = []
        for annot in zotero_annotations:
            try:
                if len(annot.text) >= 8191:
                    print(
                        f"A Zotero annotation from an item with {annot.title} (item_key={annot.key} and "
                        f"version={annot.version}) cannot be uploaded since the highlight/note is very long. "
                        f"A Readwise highlight can be up to 8191 characters."
                    )
                    failed_item = annot.get_nonempty_params()
                    failed_item["error_type"] = "CharacterLimitExceeded"
                    failed_item["error_message"] = (
                        f"Highlight exceeds 8191 character limit ({len(annot.text)} chars)"
                    )
                    self.failed_highlights.append(failed_item)
                    continue  # Go to next annot
                rw_highlight = self.convert_zotero_annotation_to_readwise_highlight(annot)
            except Exception as e:
                # Store failed item with error details for better debugging
                failed_item = annot.get_nonempty_params()
                failed_item["error_type"] = type(e).__name__
                failed_item["error_message"] = str(e)
                self.failed_highlights.append(failed_item)
                print(f"Warning: Failed to convert item {annot.key}: {type(e).__name__}: {e}")
                continue  # Go to next annot
            rw_highlights.append(rw_highlight.get_nonempty_params())
        self.create_highlights(rw_highlights)

        finished_msg = ""
        if self.failed_highlights:
            finished_msg = (
                f"\nNOTE: {len(self.failed_highlights)} highlights (out of {len(self.failed_highlights)}) failed "
                f"to upload to Readwise.\n"
            )

        finished_msg += (
            f"\n{len(rw_highlights)} highlights were successfully uploaded to Readwise.\n\n"
        )
        print(finished_msg)

    def save_failed_items_to_json(self, json_filepath_failed_items: str | None = None) -> None:
        """Save failed highlights to a JSON file for debugging.

        Args:
            json_filepath_failed_items: Optional filename for the output file.
                Defaults to "failed_readwise_items.json".
        """
        FAILED_ITEMS_DIR.mkdir(parents=True, exist_ok=True)
        if json_filepath_failed_items:
            out_filepath = FAILED_ITEMS_DIR.joinpath(json_filepath_failed_items)
        else:
            out_filepath = FAILED_ITEMS_DIR.joinpath("failed_readwise_items.json")

        with open(out_filepath, "w", encoding="utf-8") as f:
            dump(self.failed_highlights, f, indent=4, ensure_ascii=False)
        print(
            f"{len(self.failed_highlights)} highlights failed to format (hence failed to upload to Readwise).\n"
            f"Detail of failed items are saved into {out_filepath}"
        )
