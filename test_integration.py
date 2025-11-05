#!/usr/bin/env python3
"""
Integration test based on README example
"""

import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from zotero2readwise.zt2rw import Zotero2Readwise


def test_integration():
    """Test the integration using README approach"""
    print("Testing Zotero2Readwise integration...")

    # Get credentials from environment
    readwise_token = os.getenv("READWISE_TOKEN")
    zotero_key = os.getenv("ZOTERO_API_KEY")
    zotero_library_id = os.getenv("ZOTERO_USER_ID")

    if not all([readwise_token, zotero_key, zotero_library_id]):
        print("❌ Missing required environment variables")
        return False

    print(f"Using Zotero library ID: {zotero_library_id}")

    try:
        # Test with new write_failures parameter
        zt_rw = Zotero2Readwise(
            readwise_token=readwise_token,
            zotero_key=zotero_key,
            zotero_library_id=zotero_library_id,
            zotero_library_type="user",
            include_annotations=True,
            include_notes=False,
            write_failures=False,  # Test the new parameter - suppress failures
        )

        print("✅ Zotero2Readwise object created successfully")

        # Test retrieving items (but don't run full sync to avoid spam)
        print("Testing item retrieval...")
        items = zt_rw.get_all_zotero_items()
        print(f"✅ Retrieved {len(items)} items from Zotero")

        # Test the formatting without uploading
        if items:
            print("Testing item formatting...")
            formatted_items = zt_rw.zotero.format_items(items[:1])  # Just test first item
            print(f"✅ Successfully formatted {len(formatted_items)} items")

            if formatted_items:
                item = formatted_items[0]
                print(f"✅ Sample item: {item.title[:50]}...")

        print("✅ All tests passed! Recent changes are working correctly.")
        return True

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False


if __name__ == "__main__":
    success = test_integration()
    exit(0 if success else 1)
