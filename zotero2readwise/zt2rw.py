from typing import Dict, List

from zotero2readwise.readwise import Readwise
from zotero2readwise.zotero import (
    ZoteroAnnotationsNotes,
    get_zotero_client,
    retrieve_all_annotations,
    retrieve_all_notes,
)


class Zotero2Readwise:
    def __init__(
        self,
        readwise_token: str,
        zotero_key: str,
        zotero_library_id: str,
        zotero_library_type: str = "user",
        include_annotations: bool = True,
        include_notes: bool = False,
    ):

        self.readwise = Readwise(readwise_token)
        self.zotero_client = get_zotero_client(
            library_id=zotero_library_id,
            library_type=zotero_library_type,
            api_key=zotero_key,
        )
        self.zotero = ZoteroAnnotationsNotes(self.zotero_client)
        self.include_annots = include_annotations
        self.include_notes = include_notes

    def get_all_zotero_items(self) -> List[Dict]:
        annots, notes = [], []
        if self.include_annots:
            annots = retrieve_all_annotations(self.zotero_client)
        if self.include_notes:
            notes = retrieve_all_notes(self.zotero_client)
        all_zotero_items = annots + notes
        print(f"{len(all_zotero_items)} Zotero items are retrieved.")
        return all_zotero_items

    def run(self, zot_annots_notes: List[Dict] = None) -> None:
        if zot_annots_notes is None:
            zot_annots_notes = self.get_all_zotero_items()
        formatted_items = self.zotero.format_items(zot_annots_notes)
        if self.zotero.failed_items:
            self.zotero.save_failed_items_to_json("failed_zotero_items.json")

        self.readwise.post_zotero_annotations_to_readwise(formatted_items)
