from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Union

import requests
from pyzotero.zotero import Zotero

from zt2rw.helper import sanitize_tag
from zt2rw.zotero import ZoteroAnnotationsNotes


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
    location: Optional[int] = None
    location_type: Optional[str] = None
    highlighted_at: Optional[str] = None
    highlight_url: Optional[str] = None

    def get_nonempty_params(self) -> Dict:
        return {k: v for k, v in self.__dict__.items() if v}


class Readwise:
    def __init__(self, readwise_token: str, zotero_client: Zotero):
        self._token = readwise_token
        self._header = {"Authorization": f"Token {self._token}"}
        self.endpoints = ReadwiseAPI
        self.zot = ZoteroAnnotationsNotes(zotero_client)

    def create_highlights(self, highlights: List[Dict]) -> None:
        requests.post(
            url=self.endpoints.highlights,
            headers=self._header,
            json={"highlights": highlights},
        )

    @staticmethod
    def convert_tags_to_readwise_format(tags: List[Dict]) -> str:
        flattened_tags = [d_["tag"] for d_ in tags]
        return " ".join([f".{sanitize_tag(tag.lower())}" for tag in flattened_tags])

    def format_readwise_note(self, tags, comment) -> Union[str, None]:
        tags = self.convert_tags_to_readwise_format(tags)
        highlight_note = ""
        if tags:
            highlight_note += tags + "\n"
        if comment:
            highlight_note += comment
        return highlight_note if highlight_note else None

    def convert_zotero_annotation_to_readwise_highlight(
        self, zotero_annot: Dict
    ) -> ReadwiseHighlight:
        data = zotero_annot["data"]
        metadata = self.zot.get_item_metadata(zotero_annot)
        highlight_note = self.format_readwise_note(
            tags=data["tags"], comment=data["annotationComment"]
        )
        return ReadwiseHighlight(
            text=data["annotationText"],
            title=metadata["title"],
            note=highlight_note,
            author=metadata.get(metadata["creators"]),
            category=Category.articles.name
            if metadata["item_type"] != "book"
            else Category.books.name,
            highlighted_at=data["dateModified"],
            source_url=metadata["source_url"] if metadata["source_url"] else None,
            highlight_url=metadata["source_url"],
        )
