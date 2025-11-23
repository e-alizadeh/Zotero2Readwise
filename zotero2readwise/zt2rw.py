"""Main orchestrator module for syncing Zotero annotations to Readwise.

This module provides the Zotero2Readwise class which coordinates the entire
synchronization process between Zotero and Readwise.

Example:
    >>> from zotero2readwise.zt2rw import Zotero2Readwise
    >>> zt_rw = Zotero2Readwise(
    ...     readwise_token="your_token",
    ...     zotero_key="your_key",
    ...     zotero_library_id="your_id",
    ... )
    >>> zt_rw.run()
"""

from collections.abc import Sequence

from zotero2readwise.readwise import Readwise
from zotero2readwise.zotero import (
    ZoteroAnnotationsNotes,
    get_zotero_client,
)


class Zotero2Readwise:
    """Main orchestrator class for syncing Zotero annotations and notes to Readwise.

    This class coordinates the entire synchronization process:
    1. Retrieves annotations and/or notes from Zotero API
    2. Formats them into a standardized format
    3. Uploads them to Readwise as highlights

    Attributes:
        readwise: Readwise client instance for uploading highlights.
        zotero_client: Pyzotero client instance for Zotero API access.
        zotero: ZoteroAnnotationsNotes instance for formatting Zotero items.
        include_annots: Whether to include annotations in sync.
        include_notes: Whether to include notes in sync.
        since: Unix timestamp to filter items modified after this time.
        write_failures: Whether to save failed items to JSON files.

    Example:
        >>> zt_rw = Zotero2Readwise(
        ...     readwise_token="rw_token",
        ...     zotero_key="zot_key",
        ...     zotero_library_id="12345",
        ...     include_annotations=True,
        ...     include_notes=True,
        ... )
        >>> zt_rw.run()
    """

    def __init__(
        self,
        readwise_token: str,
        zotero_key: str,
        zotero_library_id: str,
        zotero_library_type: str = "user",
        include_annotations: bool = True,
        include_notes: bool = False,
        filter_colors: Sequence[str] = (),
        filter_tags: Sequence[str] = (),
        include_filter_tags: bool = False,
        since: int = 0,
        write_failures: bool = True,
        custom_tag: str | None = None,
    ):
        """Initialize the Zotero2Readwise synchronizer.

        Args:
            readwise_token: Readwise API access token.
            zotero_key: Zotero API key.
            zotero_library_id: Zotero library ID (user ID or group ID).
            zotero_library_type: Type of Zotero library, either "user" or "group".
            include_annotations: Whether to sync Zotero annotations (highlights/comments).
            include_notes: Whether to sync Zotero standalone notes.
            filter_colors: Only include annotations with these highlight colors (hex codes).
            filter_tags: Only include annotations with these tags.
            include_filter_tags: If True, include filter tags in the synced items.
            since: Unix timestamp; only sync items modified after this time.
            write_failures: If True, save failed items to JSON files for debugging.
            custom_tag: Optional custom tag to add to all Readwise highlights.
        """
        self.readwise = Readwise(readwise_token, custom_tag=custom_tag)
        self.zotero_client = get_zotero_client(
            library_id=zotero_library_id,
            library_type=zotero_library_type,
            api_key=zotero_key,
        )
        self.zotero = ZoteroAnnotationsNotes(
            self.zotero_client, filter_colors, filter_tags, include_filter_tags
        )
        self.include_annots = include_annotations
        self.include_notes = include_notes
        self.since = since
        self.write_failures = write_failures

    def get_all_zotero_items(self) -> list[dict]:
        """
        Retrieves all Zotero items of the specified types (notes and/or annotations) that were modified since the specified date.

        Returns:
        A list of dictionaries representing the retrieved Zotero items.
        """
        items = []
        if self.include_annots:
            items.extend(self.retrieve_all("annotation", self.since))

        if self.include_notes:
            items.extend(self.retrieve_all("note", self.since))

        print(f"{len(items)} Zotero items are retrieved.")

        return items

    def run(self, zot_annots_notes: list[dict] = None) -> None:
        """Execute the synchronization process.

        This method orchestrates the full sync workflow:
        1. Retrieves Zotero items (if not provided)
        2. Formats items into ZoteroItem objects
        3. Saves any failed items to JSON (if write_failures is True)
        4. Uploads formatted items to Readwise

        Args:
            zot_annots_notes: Optional list of raw Zotero annotation/note dictionaries.
                If not provided, items will be retrieved from Zotero API.
        """
        if zot_annots_notes is None:
            zot_annots_notes = self.get_all_zotero_items()

        formatted_items = self.zotero.format_items(zot_annots_notes)

        if self.write_failures and self.zotero.failed_items:
            self.zotero.save_failed_items_to_json("failed_zotero_items.json")

        self.readwise.post_zotero_annotations_to_readwise(formatted_items)

    def retrieve_all(self, item_type: str, since: int = 0):
        """
        Retrieves all items of a given type from Zotero Database since a given timestamp.

        Args:
            item_type (str): Either "annotation" or "note".
            since (int): Timestamp in seconds since the Unix epoch. Defaults to 0.

        Returns:
            List[Dict]: List of dictionaries containing the retrieved items.
        """
        if item_type not in ["annotation", "note"]:
            raise ValueError("item_type must be either 'annotation' or 'note'")

        if since == 0:
            print(f"Retrieving ALL {item_type}s from Zotero Database")
        else:
            print(f"Retrieving {item_type}s since last run from Zotero Database")

        print("It may take some time...")
        query = self.zotero_client.items(itemType=item_type, since=since)
        return self.zotero_client.everything(query)
