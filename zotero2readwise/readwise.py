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
    """Dataclass for ReadWise API endpoints"""

    base_url: str = "https://readwise.io/api/v2"
    highlights: str = base_url + "/highlights/"
    books: str = base_url + "/books/"


class Category(Enum):
    articles = 1
    books = 2
    tweets = 3
    podcasts = 4


@dataclass
class ReadwiseHighlight:
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
        if not self.location:
            self.location = None

    def get_nonempty_params(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if v}


class Readwise:
    def __init__(self, readwise_token: str, custom_tag: str | None = None):
        self._token = readwise_token
        self._header = {"Authorization": f"Token {self._token}"}
        self.endpoints = ReadwiseAPI
        self.failed_highlights: list = []
        self.custom_tag = custom_tag  # Optional tag to add to all highlights (e.g., "zotero")

    def create_highlights(self, highlights: list[dict]) -> None:
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
    def convert_tags_to_readwise_format(tags: list[str]) -> str:
        return " ".join([f".{sanitize_tag(t.lower())}" for t in tags])

    def format_readwise_note(self, tags, comment) -> str | None:
        rw_tags = self.convert_tags_to_readwise_format(tags)
        highlight_note = ""
        # Add custom tag if configured (e.g., ".zotero")
        if self.custom_tag:
            highlight_note += f".{sanitize_tag(self.custom_tag.lower())} "
        if rw_tags:
            highlight_note += rw_tags + "\n"
        elif self.custom_tag:
            highlight_note += "\n"  # Add newline after custom tag if no other tags
        if comment:
            highlight_note += comment
        return highlight_note.strip() if highlight_note.strip() else None

    def convert_zotero_annotation_to_readwise_highlight(
        self, annot: ZoteroItem
    ) -> ReadwiseHighlight:
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

    def save_failed_items_to_json(self, json_filepath_failed_items: str = None):
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
