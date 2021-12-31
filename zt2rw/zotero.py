from dataclasses import dataclass, field
from os import environ
from typing import Dict, List, Optional

from pyzotero.zotero import Zotero
from pyzotero.zotero_errors import ParamNotPassed, UnsupportedParams


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
    tags: Optional[List[Dict]] = field(init=True, default=None)
    document_tags: Optional[List[Dict]] = field(init=True, default=None)
    document_type: Optional[int] = None
    annotation_type: Optional[str] = None
    creators: Optional[List[str]] = field(init=True, default=None)
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
        self.cache: Dict = {}
        self.parent_mapping: Dict = {}

    def get_item_metadata(self, annot: Dict) -> Dict:
        data = annot["data"]
        # A Zotero annotation or note must have a parent with parentItem key.
        parent_item_key = data["parentItem"]

        if parent_item_key in self.parent_mapping:
            top_item_key = self.parent_mapping[parent_item_key]
            if top_item_key in self.cache:
                return self.cache[top_item_key]
        else:
            parent_item = self.zot.item(parent_item_key)
            top_item_key = parent_item["data"].get("parentItem", None)
            self.parent_mapping[parent_item_key] = (
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

        self.cache[top_item_key] = metadata
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
            creators=data.get("creators"),
            source_url=metadata["source_url"],
            page_label=data.get("annotationPageLabel"),
            color=data.get("annotationColor"),
            relations=data["relations"],
        )

    def format_items(self, annots: List[Dict]) -> List[ZoteroItem]:
        formatted_annots = []
        for annot in annots:
            try:
                formatted_annots.append(self.format_item(annot))
            except:
                self.failed_items.append(annot)
                continue
        return formatted_annots
