from enum import Enum
from typing import Dict, Optional, List

import requests
from dataclasses import dataclass


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
    source_url: Optional[str] = Category.articles
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
    def __init__(
        self,
        access_token: str,
    ):
        self._token = access_token
        self._header = {"Authorization": f"Token {self._token}"}
        self.endpoints = ReadwiseAPI

    def format_highlights(self) -> List[Dict]:
        pass

    def create_highlight(self, highlights: List[Dict]) -> None:
        requests.post(
            url=self.endpoints.highlights,
            headers=self._header,
            json={"highlights": highlights}
        )



from json import load

from zt2rw.zotero import get_zotero_client

if __name__ == "__main__":
    zot = get_zotero_client(library_id="8135490", api_key="buZVNxNzHcXx3VHdbO7HWwe2")

    with open("./zt2rw/all_annotations.json", "r") as f:
        annots = load(f)


