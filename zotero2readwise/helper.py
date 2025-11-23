"""Helper utility functions for Zotero2Readwise.

This module provides utility functions for tag sanitization and
library version management (for incremental sync support).
"""

from pyzotero.zotero import Zotero


def sanitize_tag(tag: str) -> str:
    """Clean tag by stripping whitespace and replacing spaces with underscores.

    Args:
        tag: The tag string to sanitize.

    Returns:
        Cleaned tag with leading/trailing whitespace removed and
        internal spaces replaced with underscores.

    Example:
        >>> sanitize_tag(" Machine Learning ")
        'Machine_Learning'
    """
    return tag.strip().replace(" ", "_")


def read_library_version() -> int:
    """Read the library version from the 'since' file.

    The 'since' file stores the last sync timestamp/version number,
    enabling incremental syncs that only process new items.

    Returns:
        The library version as an integer, or 0 if the file doesn't
        exist or contains invalid data.
    """
    try:
        with open("since", encoding="utf-8") as file:
            return int(file.read())
    except FileNotFoundError:
        print("since file does not exist, using library version 0")
    except ValueError:
        print("since file does not include a number, using library version 0")
    return 0


def write_library_version(zotero_client: Zotero) -> None:
    """Write the current library version to the 'since' file.

    Saves the last modified version from the Zotero client, enabling
    future incremental syncs to start from this point.

    Args:
        zotero_client: A Pyzotero Zotero client instance.
    """
    with open("since", "w", encoding="utf-8") as file:
        file.write(str(zotero_client.last_modified_version()))
