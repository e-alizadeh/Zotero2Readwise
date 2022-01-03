from dataclasses import dataclass
from enum import Enum
from json import dump
from typing import Dict, List, Optional, Union

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
    title: Optional[str] = None
    author: Optional[str] = None
    image_url: Optional[str] = None
    source_url: Optional[str] = Category.articles.name
    source_type: Optional[str] = None
    category: Optional[str] = None
    note: Optional[str] = None
    location: Union[int, None] = 0
    location_type: Optional[str] = "page"
    highlighted_at: Optional[str] = None
    highlight_url: Optional[str] = None

    def __post_init__(self):
        if not self.location:
            self.location = None

    def get_nonempty_params(self) -> Dict:
        return {k: v for k, v in self.__dict__.items() if v}


class Readwise:
    def __init__(self, readwise_token: str):
        self._token = readwise_token
        self._header = {"Authorization": f"Token {self._token}"}
        self.endpoints = ReadwiseAPI
        self.failed_highlights: List = []

    def create_highlights(self, highlights: List[Dict]) -> None:
        resp = requests.post(
            url=self.endpoints.highlights,
            headers=self._header,
            json={"highlights": highlights},
        )
        if resp.status_code != 200:
            error_log_file = (
                f"error_log_{resp.status_code}_failed_post_request_to_readwise.json"
            )
            with open(error_log_file, "w") as f:
                dump(resp.json(), f)
            raise Zotero2ReadwiseError(
                f"Uploading to Readwise failed with following details:\n"
                f"POST request Status Code={resp.status_code} ({resp.reason})\n"
                f"Error log is saved to {error_log_file} file."
            )

    @staticmethod
    def convert_tags_to_readwise_format(tags: List[str]) -> str:
        return " ".join([f".{sanitize_tag(t.lower())}" for t in tags])

    def format_readwise_note(self, tags, comment) -> Union[str, None]:
        rw_tags = self.convert_tags_to_readwise_format(tags)
        highlight_note = ""
        if rw_tags:
            highlight_note += rw_tags + "\n"
        if comment:
            highlight_note += comment
        return highlight_note if highlight_note else None

    def convert_zotero_annotation_to_readwise_highlight(
        self, annot: ZoteroItem
    ) -> ReadwiseHighlight:

        highlight_note = self.format_readwise_note(
            tags=annot.tags, comment=annot.comment
        )
        if annot.page_label and annot.page_label.isnumeric():
            location = int(annot.page_label)
        else:
            location = 0

        return ReadwiseHighlight(
            text=annot.text,
            title=annot.title,
            note=highlight_note,
            author=annot.creators,
            category=Category.articles.name
            if annot.document_type != "book"
            else Category.books.name,
            highlighted_at=annot.annotated_at,
            source_url=annot.source_url,
            highlight_url=annot.annotation_url,
            location=location,
        )

    def post_zotero_annotations_to_readwise(
        self, zotero_annotations: List[ZoteroItem]
    ) -> None:
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
                    self.failed_highlights.append(annot.get_nonempty_params())
                    continue  # Go to next annot
                rw_highlight = self.convert_zotero_annotation_to_readwise_highlight(
                    annot
                )
            except:
                self.failed_highlights.append(annot.get_nonempty_params())
                continue  # Go to next annot
            rw_highlights.append(rw_highlight.get_nonempty_params())
        self.create_highlights(rw_highlights)

        finished_msg = ""
        if self.failed_highlights:
            finished_msg = (
                f"\nNOTE: {len(self.failed_highlights)} highlights (out of {len(self.failed_highlights)}) failed "
                f"to upload to Readwise.\n"
            )

        finished_msg += f"\n{len(rw_highlights)} highlights were successfully uploaded to Readwise.\n\n"
        print(finished_msg)

    def save_failed_items_to_json(self, json_filepath_failed_items: str = None):
        FAILED_ITEMS_DIR.mkdir(parents=True, exist_ok=True)
        if json_filepath_failed_items:
            out_filepath = FAILED_ITEMS_DIR.joinpath(json_filepath_failed_items)
        else:
            out_filepath = FAILED_ITEMS_DIR.joinpath("failed_readwise_items.json")

        with open(out_filepath, "w") as f:
            dump(self.failed_highlights, f)
        print(
            f"{len(self.failed_highlights)} highlights failed to format (hence failed to upload to Readwise).\n"
            f"Detail of failed items are saved into {out_filepath}"
        )
