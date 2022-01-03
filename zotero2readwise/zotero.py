from dataclasses import dataclass, field
from json import dump
from os import environ
from typing import Dict, List, Optional

from pyzotero.zotero import Zotero
from pyzotero.zotero_errors import ParamNotPassed, UnsupportedParams

from zotero2readwise import FAILED_ITEMS_DIR


@dataclass
class ZoteroItem:
    key: str
    version: int
    item_type: str
    text: str
    annotated_at: str
    annotation_url: str
    comment: Optional[str] = None
    title: Optional[str] = None
    tags: Optional[List[str]] = field(init=True, default=None)
    document_tags: Optional[List[Dict]] = field(init=True, default=None)
    document_type: Optional[int] = None
    annotation_type: Optional[str] = None
    creators: Optional[str] = field(init=True, default=None)
    source_url: Optional[str] = None
    page_label: Optional[str] = None
    color: Optional[str] = None
    relations: Optional[Dict] = field(init=True, default=None)

    def __post_init__(self):
        # Convert [{'tag': 'abc'}, {'tag': 'def'}] -->  ['abc', 'def']
        if self.tags:
            self.tags = [d_["tag"] for d_ in self.tags]

        if self.document_tags:
            self.document_tags = [d_["tag"] for d_ in self.document_tags]

        # Sample {'dc:relation': ['http://zotero.org/users/123/items/ABC', 'http://zotero.org/users/123/items/DEF']}
        if self.relations:
            self.relations = self.relations.get("dc:relation")

        self.creators = ", ".join(self.creators) if self.creators else None

    def get_nonempty_params(self) -> Dict:
        return {k: v for k, v in self.__dict__.items() if v}


def get_zotero_client(
    library_id: str = None, api_key: str = None, library_type: str = "user"
) -> Zotero:
    """Create a Zotero client object from Pyzotero library

    Zotero userID and Key are available

    Parameters
    ----------
    library_id: str
        If not passed, then it looks for `ZOTERO_LIBRARY_ID` in the environment variables.
    api_key: str
        If not passed, then it looks for `ZOTERO_KEY` in the environment variables.
    library_type: str ['user', 'group']
        'user': to access your Zotero library
        'group': to access a shared group library

    Returns
    -------
    Zotero
        a Zotero client object
    """

    if library_id is None:
        try:
            library_id = environ["ZOTERO_LIBRARY_ID"]
        except KeyError:
            raise ParamNotPassed(
                "No value for library_id is found. "
                "You can set it as an environment variable `ZOTERO_LIBRARY_ID` or use `library_id` to set it."
            )

    if api_key is None:
        try:
            api_key = environ["ZOTERO_KEY"]
        except KeyError:
            raise ParamNotPassed(
                "No value for api_key is found. "
                "You can set it as an environment variable `ZOTERO_KEY` or use `api_key` to set it."
            )

    if library_type is None:
        library_type = environ.get("LIBRARY_TYPE", "user")
    elif library_type not in ["user", "group"]:
        raise UnsupportedParams("library_type value can either be 'user' or 'group'.")

    return Zotero(
        library_id=library_id,
        library_type=library_type,
        api_key=api_key,
    )


class ZoteroAnnotationsNotes:
    def __init__(self, zotero_client: Zotero):
        self.zot = zotero_client
        self.failed_items: List[Dict] = []
        self._cache: Dict = {}
        self._parent_mapping: Dict = {}

    def get_item_metadata(self, annot: Dict) -> Dict:
        data = annot["data"]
        # A Zotero annotation or note must have a parent with parentItem key.
        parent_item_key = data["parentItem"]

        if parent_item_key in self._parent_mapping:
            top_item_key = self._parent_mapping[parent_item_key]
            if top_item_key in self._cache:
                return self._cache[top_item_key]
        else:
            parent_item = self.zot.item(parent_item_key)
            top_item_key = parent_item["data"].get("parentItem", None)
            self._parent_mapping[parent_item_key] = (
                top_item_key if top_item_key else parent_item_key
            )

        if top_item_key:
            top_item = self.zot.item(top_item_key)
            data = top_item["data"]
        else:
            top_item = parent_item
            data = top_item["data"]
            top_item_key = data["key"]

        metadata = {
            "title": data["title"],
            # "date": data["date"],
            "tags": data["tags"],
            "document_type": data["itemType"],
            "source_url": top_item["links"]["self"]["href"],
        }
        if "creators" in data:
            metadata["creators"] = [
                creator["firstName"] + " " + creator["lastName"]
                for creator in data["creators"]
            ]

        self._cache[top_item_key] = metadata
        return metadata

    def format_item(self, annot: Dict) -> ZoteroItem:
        data = annot["data"]
        item_type = data["itemType"]
        annotation_type = data.get("annotationType")
        metadata = self.get_item_metadata(annot)

        text = ""
        comment = ""
        if item_type == "annotation":
            if annotation_type == "highlight":
                text = data["annotationText"]
                comment = data["annotationComment"]
            elif annotation_type == "note":
                text = data["annotationComment"]
                comment = ""
        elif item_type == "note":
            text = data["note"]
            comment = ""
        else:
            raise NotImplementedError(
                "Only Zotero item types of 'note' and 'annotation' are supported."
            )

        if text == "":
            raise ValueError("No annotation or note data is found.")
        return ZoteroItem(
            key=data["key"],
            version=data["version"],
            item_type=item_type,
            text=text,
            annotated_at=data["dateModified"],
            annotation_url=annot["links"]["self"]["href"],
            comment=comment,
            title=metadata["title"],
            tags=data["tags"],
            document_tags=metadata["tags"],
            document_type=metadata["document_type"],
            annotation_type=annotation_type,
            creators=metadata.get("creators"),
            source_url=metadata["source_url"],
            page_label=data.get("annotationPageLabel"),
            color=data.get("annotationColor"),
            relations=data["relations"],
        )

    def format_items(self, annots: List[Dict]) -> List[ZoteroItem]:
        formatted_annots = []
        print(
            f"ZOTERO: Start formatting {len(annots)} annotations/notes...\n"
            f"It may take some time depending on the number of annotations...\n"
            f"A complete message will show up once it's done!\n"
        )
        for annot in annots:
            try:
                formatted_annots.append(self.format_item(annot))
            except:
                self.failed_items.append(annot)
                continue

        finished_msg = "\nZOTERO: Formatting Zotero Items is completed!!\n\n"
        if self.failed_items:
            finished_msg += (
                f"\nNOTE: {len(self.failed_items)} Zotero annotations/notes (out of {len(annots)}) failed to format.\n"
                f"You can run `save_failed_items_to_json()` class method to save those items."
            )
        print(finished_msg)
        return formatted_annots

    def save_failed_items_to_json(self, json_filepath_failed_items: str = None):
        FAILED_ITEMS_DIR.mkdir(parents=True, exist_ok=True)
        if json_filepath_failed_items:
            out_filepath = FAILED_ITEMS_DIR.joinpath(json_filepath_failed_items)
        else:
            out_filepath = FAILED_ITEMS_DIR.joinpath("failed_zotero_items.json")
        with open(out_filepath, "w") as f:
            dump(self.failed_items, f)
        print(f"\nZOTERO: Detail of failed items are saved into {out_filepath}\n")


def retrieve_all_annotations(zotero_client: Zotero) -> List[Dict]:
    print(
        "Retrieving ALL annotations from Zotero Database. \nIt may take some time...\n"
    )
    return zotero_client.everything(zotero_client.items(itemType="annotation"))


def retrieve_all_notes(zotero_client: Zotero) -> List[Dict]:
    print("Retrieving ALL notes from Zotero Database. \nIt may take some time...\n")
    return zotero_client.everything(zotero_client.items(itemType="note"))
