import os
from pathlib import Path

__author__ = "Essi Alizadeh"
__version__ = "1.3.0"

TOP_DIR = Path(__file__).parent
# If TOP_DIR is readonly os with nix,
# then failed_zotero_items.json is written to the working directory instead.
FAILED_ITEMS_DIR = TOP_DIR if os.access(TOP_DIR, os.W_OK) else Path.cwd()
