"""Pytest configuration and shared fixtures."""

import pytest
from unittest.mock import Mock, MagicMock
from datetime import datetime


@pytest.fixture
def mock_zotero_client():
    """Create a mock Zotero client."""
    client = Mock()
    client.last_modified_version.return_value = 12345
    return client


@pytest.fixture
def sample_zotero_annotation():
    """Create a sample Zotero annotation data structure."""
    return {
        "key": "ABC123",
        "version": 100,
        "data": {
            "key": "ABC123",
            "version": 100,
            "itemType": "annotation",
            "annotationType": "highlight",
            "annotationText": "This is a sample highlight text",
            "annotationComment": "This is a comment",
            "annotationColor": "#ffd400",
            "annotationPageLabel": "10",
            "parentItem": "PARENT123",
            "dateModified": "2023-01-01T12:00:00Z",
            "tags": [{"tag": "important"}, {"tag": "machine learning"}],
            "relations": {},
        },
        "links": {
            "alternate": {"href": "https://www.zotero.org/users/123/items/ABC123"}
        },
    }


@pytest.fixture
def sample_zotero_note():
    """Create a sample Zotero note data structure."""
    return {
        "key": "NOTE123",
        "version": 101,
        "data": {
            "key": "NOTE123",
            "version": 101,
            "itemType": "note",
            "note": "<p>This is a sample note</p>",
            "parentItem": "PARENT123",
            "dateModified": "2023-01-02T12:00:00Z",
            "tags": [{"tag": "note"}],
            "relations": {},
        },
        "links": {
            "alternate": {"href": "https://www.zotero.org/users/123/items/NOTE123"}
        },
    }


@pytest.fixture
def sample_parent_item():
    """Create a sample parent item (paper/book)."""
    return {
        "key": "PARENT123",
        "version": 99,
        "data": {
            "key": "PARENT123",
            "version": 99,
            "itemType": "journalArticle",
            "title": "Sample Research Paper",
            "date": "2023",
            "creators": [
                {"firstName": "John", "lastName": "Doe"},
                {"firstName": "Jane", "lastName": "Smith"},
            ],
            "tags": [{"tag": "research"}],
        },
        "links": {
            "alternate": {"href": "https://www.zotero.org/users/123/items/PARENT123"},
            "attachment": {
                "href": "https://www.zotero.org/users/123/items/ATTACH123",
                "attachmentType": "application/pdf",
            },
        },
    }


@pytest.fixture
def readwise_token():
    """Sample Readwise API token."""
    return "test_readwise_token_12345"


@pytest.fixture
def zotero_credentials():
    """Sample Zotero credentials."""
    return {
        "key": "test_zotero_key",
        "library_id": "123456",
        "library_type": "user",
    }
