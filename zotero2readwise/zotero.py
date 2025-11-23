"""Zotero API interaction module.

This module provides classes and functions for interacting with the Zotero API
to retrieve and format annotations and notes.

Classes:
    ZoteroItem: Dataclass representing a formatted Zotero annotation or note.
    ZoteroAnnotationsNotes: Handler for retrieving and formatting Zotero items.

Functions:
    get_zotero_client: Create a Pyzotero client instance.
"""

from collections.abc import Sequence
from dataclasses import dataclass, field
from json import dump
from os import environ

from pyzotero.zotero import Zotero

from zotero2readwise import FAILED_ITEMS_DIR


@dataclass
class ZoteroItem:
    """Dataclass representing a formatted Zotero annotation or note.

    This class standardizes the representation of Zotero items for processing
    and conversion to Readwise highlights.

    Attributes:
        key: Unique Zotero item key.
        version: Zotero item version number.
        item_type: Type of item ("annotation" or "note").
        text: The annotation text or note content.
        annotated_at: ISO timestamp when the item was modified.
        annotation_url: URL to the item in Zotero web library.
        comment: Optional comment/note attached to a highlight.
        title: Title of the parent document.
        tags: List of tag strings from the annotation.
        document_tags: List of tags from the parent document.
        document_type: Type of the parent document (e.g., "journalArticle", "book").
        annotation_type: Type of annotation ("highlight", "note", "ink", "image").
        creators: Formatted author string (comma-separated).
        source_url: URL to the parent item in Zotero.
        attachment_url: URL to the PDF attachment (if any).
        page_label: Page number/label where the annotation appears.
        color: Hex color code of the highlight (e.g., "#ffd400").
        relations: Related Zotero items (dc:relation).
        sort_index: Zotero's annotationSortIndex for ordering within a document.
    """

    key: str
    version: int
    item_type: str
    text: str
    annotated_at: str
    annotation_url: str
    comment: str | None = None
    title: str | None = None
    tags: list[str] | None = field(init=True, default=None)
    document_tags: list[dict] | None = field(init=True, default=None)
    document_type: int | None = None
    annotation_type: str | None = None
    creators: str | None = field(init=True, default=None)
    source_url: str | None = None
    attachment_url: str | None = None
    page_label: str | None = None
    color: str | None = None
    relations: dict | None = field(init=True, default=None)
    sort_index: str | None = None  # Zotero's annotationSortIndex for ordering

    def __post_init__(self):
        # Convert [{'tag': 'abc'}, {'tag': 'def'}] -->  ['abc', 'def']
        if self.tags:
            self.tags = [d_["tag"] for d_ in self.tags]

        if self.document_tags:
            self.document_tags = [d_["tag"] for d_ in self.document_tags]

        # Sample {'dc:relation': ['http://zotero.org/users/123/items/ABC', 'http://zotero.org/users/123/items/DEF']}
        if self.relations:
            self.relations = self.relations.get("dc:relation")

        if self.creators:
            self.creators = self.format_author_list(self.creators)

    @staticmethod
    def format_author_list(authors: list[str]) -> str:
        """Format a list of author names into a comma-separated string.

        Handles long author lists by truncating and adding "et al." when the
        total length would exceed 1024 characters.

        Args:
            authors: List of author name strings.

        Returns:
            Formatted author string, e.g., "John Doe, Jane Smith" or
            "John Doe, Jane Smith, et al." if truncated.

        Example:
            >>> ZoteroItem.format_author_list(["John Doe", "Jane Smith"])
            "John Doe, Jane Smith"
        """
        MAX_LENGTH = 1024
        MAX_AUTHOR_LENGTH = 256
        SEP = ", "
        ET_AL = " et al."

        # Truncate each author name to 256 characters. this simplifies logic considerably
        authors = [author[:MAX_AUTHOR_LENGTH] for author in authors]

        # Start with the full list of authors
        result = SEP.join(authors)

        # If the result is too long, remove authors from the end until it fits with SEP + ET_AL appended
        # There is no risk that we will run out of authors for .pop() because MAX_LENGTH >> MAX_AUTHOR_LENGTH
        # likewise we're guaranteed to be able to fit at least one author
        while len(result) > MAX_LENGTH:
            authors.pop()
            result = SEP.join(authors) + SEP + ET_AL

        return result

    def get_nonempty_params(self) -> dict:
        """Return a dictionary of non-empty/non-None attributes.

        Returns:
            Dictionary containing only attributes with truthy values.
        """
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
            raise ValueError(
                "No value for library_id is found. "
                "You can set it as an environment variable `ZOTERO_LIBRARY_ID` or use `library_id` to set it."
            )

    if api_key is None:
        try:
            api_key = environ["ZOTERO_KEY"]
        except KeyError:
            raise ValueError(
                "No value for api_key is found. "
                "You can set it as an environment variable `ZOTERO_KEY` or use `api_key` to set it."
            )

    if library_type is None:
        library_type = environ.get("LIBRARY_TYPE", "user")
    elif library_type not in ["user", "group"]:
        raise ValueError("library_type value can either be 'user' or 'group'.")

    return Zotero(
        library_id=library_id,
        library_type=library_type,
        api_key=api_key,
    )


class ZoteroAnnotationsNotes:
    """Handler for retrieving and formatting Zotero annotations and notes.

    This class manages the formatting of raw Zotero API responses into
    standardized ZoteroItem objects, with support for filtering by color
    and tags.

    Attributes:
        zot: Pyzotero client instance.
        failed_items: List of items that failed to format.
        filter_colors: Hex color codes to filter annotations by.
        filter_tags: Tag names to filter annotations by.
        include_filter_tags: Whether to include filter tags in output.

    Example:
        >>> zan = ZoteroAnnotationsNotes(
        ...     zotero_client,
        ...     filter_colors=["#ffd400"],
        ...     filter_tags=["important"],
        ... )
        >>> formatted = zan.format_items(raw_annotations)
    """

    def __init__(
        self,
        zotero_client: Zotero,
        filter_colors: Sequence[str],
        filter_tags: Sequence[str],
        include_filter_tags: bool = False,
    ):
        """Initialize the ZoteroAnnotationsNotes handler.

        Args:
            zotero_client: Pyzotero Zotero client instance.
            filter_colors: Sequence of hex color codes to filter by.
            filter_tags: Sequence of tag names to filter by.
            include_filter_tags: If True, include filter tags in the output items.
        """
        self.zot = zotero_client
        self.failed_items: list[dict] = []
        self._cache: dict = {}
        self._parent_mapping: dict = {}
        self.filter_colors: Sequence[str] = filter_colors
        self.filter_tags: Sequence[str] = filter_tags
        self.include_filter_tags: bool = include_filter_tags

    def get_item_metadata(self, annot: dict) -> dict:
        """Retrieve metadata for an annotation's parent document.

        Fetches and caches metadata from the parent item (and top-level item
        if the parent is an attachment) including title, authors, tags, and URLs.

        Args:
            annot: Raw Zotero annotation dictionary from API.

        Returns:
            Dictionary containing document metadata with keys:
            - title: Document title
            - tags: List of tag dictionaries
            - document_type: Zotero item type
            - source_url: Link to item in Zotero
            - creators: List of author names
            - attachment_url: Link to PDF attachment (if available)
        """
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
            "source_url": top_item["links"]["alternate"]["href"],
            "creators": "",
            "attachment_url": "",
        }
        if "creators" in data:
            metadata["creators"] = [
                # Some creators have firstName/lastName, others have single 'name' field
                # (e.g., institutional authors like "World Health Organization")
                (
                    f"{creator['firstName']} {creator['lastName']}"
                    if "firstName" in creator and "lastName" in creator
                    else creator.get("name", "Unknown")
                )
                for creator in data["creators"]
            ]
        if (
            "attachment" in top_item["links"]
            and top_item["links"]["attachment"]["attachmentType"] == "application/pdf"
        ):
            metadata["attachment_url"] = top_item["links"]["attachment"]["href"]

        self._cache[top_item_key] = metadata
        return metadata

    def format_item(self, annot: dict) -> ZoteroItem:
        """Format a single Zotero annotation or note into a ZoteroItem.

        Args:
            annot: Raw Zotero annotation/note dictionary from API.

        Returns:
            Formatted ZoteroItem instance.

        Raises:
            NotImplementedError: If the annotation type is not supported
                (ink, image annotations) or item type is unsupported.
            ValueError: If the annotation/note has no text content.
        """
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
            elif annotation_type == "ink":
                raise NotImplementedError(
                    "Handwritten (ink) annotations are not currently supported."
                )
            elif annotation_type == "image":
                raise NotImplementedError("Image/area annotations are not currently supported.")
            else:
                raise NotImplementedError(
                    f"Annotation type '{annotation_type}' is not currently supported."
                )
        elif item_type == "note":
            text = data["note"]
            comment = ""
        else:
            raise NotImplementedError(
                "Only Zotero item types of 'note' and 'annotation' are supported."
            )

        if text == "":
            raise ValueError("No annotation or note data is found.")

        exclude_tags_set = set(self.filter_tags)

        if self.include_filter_tags:
            tags = data["tags"]
        else:
            tags = (
                [t for t in data["tags"] if t["tag"] not in exclude_tags_set]
                if data["tags"]
                else data["tags"]
            )

        return ZoteroItem(
            key=data["key"],
            version=data["version"],
            item_type=item_type,
            text=text,
            annotated_at=data["dateModified"],
            annotation_url=annot["links"]["alternate"]["href"],
            attachment_url=metadata["attachment_url"],
            comment=comment,
            title=metadata["title"],
            tags=tags,
            document_tags=metadata["tags"],
            document_type=metadata["document_type"],
            annotation_type=annotation_type,
            creators=metadata.get("creators"),
            source_url=metadata["source_url"],
            page_label=data.get("annotationPageLabel"),
            color=data.get("annotationColor"),
            relations=data["relations"],
            sort_index=data.get("annotationSortIndex"),
        )

    def format_items(self, annots: list[dict]) -> list[ZoteroItem]:
        """Format multiple Zotero annotations/notes into ZoteroItems.

        Processes each annotation, applying color and tag filters, and handles
        errors gracefully by adding failed items to the failed_items list.

        Args:
            annots: List of raw Zotero annotation/note dictionaries.

        Returns:
            List of successfully formatted ZoteroItem instances, sorted by
            title and then by sort_index (reading order within each document).
        """
        formatted_annots = []
        print(
            f"ZOTERO: Start formatting {len(annots)} annotations/notes...\n"
            f"It may take some time depending on the number of annotations...\n"
            f"A complete message will show up once it's done!\n"
        )
        for annot in annots:
            try:
                color_condition = (
                    len(self.filter_colors) == 0
                    or annot["data"]["annotationColor"] in self.filter_colors
                )
                tag_condition = len(self.filter_tags) == 0 or any(
                    tag["tag"] in self.filter_tags for tag in annot["data"]["tags"]
                )
                if color_condition and tag_condition:
                    formatted_annots.append(self.format_item(annot))
            except Exception as e:
                # Store failed item with error details for better debugging
                failed_item = {
                    "item": annot,
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                }
                self.failed_items.append(failed_item)
                item_key = annot.get("data", {}).get("key", "unknown")
                print(f"Warning: Failed to format item {item_key}: {type(e).__name__}: {e}")
                continue

        # Sort annotations by title (grouping by document) and then by sort_index
        # (reading order within each document). This ensures highlights appear
        # in chronological sequence within each document in Readwise.
        formatted_annots.sort(key=lambda x: (x.title or "", x.sort_index or ""))

        finished_msg = "\nZOTERO: Formatting Zotero Items is completed!!\n\n"
        if self.failed_items:
            finished_msg += (
                f"\nNOTE: {len(self.failed_items)} Zotero annotations/notes (out of {len(annots)}) failed to format.\n"
                f"You can run `save_failed_items_to_json()` class method to save those items."
            )
        print(finished_msg)
        return formatted_annots

    def save_failed_items_to_json(self, json_filepath_failed_items: str = None) -> None:
        """Save failed items to a JSON file for debugging.

        Args:
            json_filepath_failed_items: Optional filename for the output file.
                Defaults to "failed_zotero_items.json".
        """
        FAILED_ITEMS_DIR.mkdir(parents=True, exist_ok=True)
        if json_filepath_failed_items:
            out_filepath = FAILED_ITEMS_DIR.joinpath(json_filepath_failed_items)
        else:
            out_filepath = FAILED_ITEMS_DIR.joinpath("failed_zotero_items.json")

        with open(out_filepath, "w", encoding="utf-8") as f:
            dump(self.failed_items, f, indent=4, ensure_ascii=False)
        print(f"\nZOTERO: Detail of failed items are saved into {out_filepath}\n")
