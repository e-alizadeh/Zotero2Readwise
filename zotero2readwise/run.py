from argparse import ArgumentParser
from distutils.util import strtobool

from zotero2readwise.zt2rw import Zotero2Readwise

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
        "zotero_library_id",
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

    zt2rw = Zotero2Readwise(
        readwise_token=args["readwise_token"],
        zotero_key=args["zotero_key"],
        zotero_library_id=args["zotero_library_id"],
        zotero_library_type=args["library_type"],
        include_annotations=args["include_annotations"],
        include_notes=args["include_notes"],
    )
    zt2rw.run_all()
