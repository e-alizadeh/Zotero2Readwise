def sanitize_tag(tag: str) -> str:
    """Clean tag by replacing empty spaces with underscore.

    Parameters
    ----------
    tag: str

    Returns
    -------
    str
        Cleaned tag

    Examples
    --------
    >>> sanitize_tag(" Machine Learning ")
    "Machine_Learning"

    """
    return tag.strip().replace(" ", "_")

def read_library_version():
    """
    Reads the library version from the 'since' file and returns it as an integer.
    If the file does not exist or does not include a number, returns 0.
    """
    try:
        with open('since', 'r', encoding='utf-8') as file:
            return int(file.read())
    except FileNotFoundError:
        print("since file does not exist, using library version 0")
    except ValueError:
        print("since file does not include a number, using library version 0")
    return 0

def write_library_version(zotero_client):
    """
    Writes the library version of the given Zotero client to a file named 'since'.

    Args:
        zotero_client: A Zotero client object.

    Returns:
        None
    """
    with open('since', 'w', encoding='utf-8') as file:
        file.write(str(zotero_client.last_modified_version()))