from argparse import ArgumentParser
from distutils.util import strtobool
from typing import Dict, List

from zotero2readwise.readwise import Readwise
from zotero2readwise.zotero import (
    ZoteroAnnotationsNotes,
    get_zotero_client,
    retrieve_all_annotations,
    retrieve_all_notes,
)


def run(
    zot: ZoteroAnnotationsNotes, rw: Readwise, zot_annots_notes: List[Dict]
) -> None:
    formatted_items = zot.format_items(zot_annots_notes)
    if zot.failed_items:
        zot.save_failed_items_to_json("failed_zotero_items.json")

    rw.post_zotero_annotations_to_readwise(formatted_items)
    if rw.failed_highlights:
        rw.save_failed_items_to_json("failed_readwise_highlights.json")


if __name__ == "__main__":
    parser = ArgumentParser(description="Generate Markdown files")
    parser.add_argument(
        "readwise_token",
        help="Readwise Access Token (visit https://readwise.io/access_token)",
    )
    parser.add_argument(
        "zotero_key", help="Zotero API key (visit https://www.zotero.org/settings/keys)"
    )
    parser.add_argument(
        "zotero_user_id",
        help="Zotero User ID (visit https://www.zotero.org/settings/keys)",
    )
    parser.add_argument(
        "--library_type",
        default="user",
        help="Zotero Library type ('user': for personal library (default value), 'group': for a shared library)",
    )
    parser.add_argument(
        "--include_annotations",
        type=str,
        default="y",
        help="Include Zotero annotations (highlights + comments) | Options: 'y'/'yes' (default), 'n'/'no'",
    )
    parser.add_argument(
        "--include_notes",
        type=str,
        default="n",
        help="Include Zotero notes | Options: 'y'/'yes' (default), 'n'/'no'",
    )

    args = vars(parser.parse_args())

    # Cast str to bool values for bool flags
    for bool_arg in ["include_annotations", "include_notes"]:
        try:
            args[bool_arg] = bool(strtobool(args[bool_arg]))
        except ValueError:
            raise ValueError(
                f"Invalid value for --{bool_arg}. Use 'n' or 'y' (default)."
            )

    # ----- Create a Zotero client object
    zot_client = get_zotero_client(
        library_id=args["zotero_user_id"],
        library_type=args["library_type"],
        api_key=args["zotero_key"],
    )

    annots = retrieve_all_annotations(zot_client)
    notes = retrieve_all_notes(zot_client)

    # Combine the list of al annots and notes
    all_zotero_items = annots + notes
    all_zotero_items = all_zotero_items[0:5] + all_zotero_items[-5:-1]

    if all_zotero_items:
        run(
            zot=ZoteroAnnotationsNotes(zot_client),
            rw=Readwise(readwise_token=args["readwise_token"]),
            zot_annots_notes=all_zotero_items,
        )
