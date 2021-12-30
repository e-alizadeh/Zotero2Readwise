from os import environ
from typing import Dict

from pyzotero.zotero import Zotero
from pyzotero.zotero_errors import ParamNotPassed, UnsupportedParams

# @dataclass
# class ZoteroAnnotation:
#     key: str
#     version: int
#     author: Optional[str] = None
#     image_url: Optional[str] = None
#     source_url: Optional[str] = None
#     source_type: Optional[str] = None
#     category: Optional[str] = None
#     note: Optional[str] = None
#     location: Optional[int] = None
#     location_type: Optional[str] = None
#     highlighted_at: Optional[str] = None
#     highlight_url: Optional[str] = None
#
#     def get_nonempty_params(self) -> Dict:
#         return {k: v for k, v in self.__dict__.items() if v}


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
            "source_url": data["url"],
            "item_type": data["itemType"],
            "annotation_url": top_item["links"]["self"]["href"],
            "location": data.get("annotationPageLabel", None),
        }
        if "creators" in data:
            creators = [
                creator["firstName"] + " " + creator["lastName"]
                for creator in data["creators"]
            ]
            metadata["creators"] = ", ".join(creators) if creators else None

        self.cache[top_item_key] = metadata
        return metadata
