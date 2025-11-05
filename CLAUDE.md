# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
Zotero2Readwise is a Python library that synchronizes Zotero annotations and notes to Readwise. It retrieves annotations from Zotero's API and uploads them to Readwise, supporting both personal and group libraries.

## Development Commands

### Setup
```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync --all-extras          # Install all dependencies including dev
uv sync                       # Install only production dependencies
```

### Code Quality
```bash
pre-commit run --all-files    # Run all code quality checks (ruff, black, mypy, etc.)
```

### Testing
```bash
# Run all tests with coverage
uv run pytest

# Run integration test (legacy)
uv run python test_integration.py
# Note: Requires environment variables: READWISE_TOKEN, ZOTERO_API_KEY, ZOTERO_USER_ID
```

### Running the Application
```bash
# Via uv script
uv run run <readwise_token> <zotero_key> <zotero_id>

# Direct Python execution
uv run python zotero2readwise/run.py <readwise_token> <zotero_key> <zotero_id>

# With Nix
nix run github:e-alizadeh/Zotero2Readwise -- <readwise_token> <zotero_key> <zotero_id>
```

## Architecture

### Core Classes
- **Zotero2Readwise** (`zt2rw.py`): Main orchestrator class that coordinates the sync process
- **ZoteroAnnotationsNotes** (`zotero.py`): Handles Zotero API interactions and data formatting
- **Readwise** (`readwise.py`): Manages Readwise API uploads and highlight formatting
- **ZoteroItem** (`zotero.py`): Dataclass representing a formatted Zotero annotation/note
- **ReadwiseHighlight** (`readwise.py`): Dataclass for Readwise highlight format

### Key Workflows
1. **Data Retrieval**: Zotero API → raw annotations/notes
2. **Formatting**: Raw data → ZoteroItem objects with metadata enrichment
3. **Conversion**: ZoteroItem → ReadwiseHighlight format
4. **Upload**: Batch upload to Readwise API

### Error Handling
- Failed Zotero items are saved to `failed_zotero_items.json`
- Failed Readwise uploads are saved to `failed_readwise_items.json`
- Use `write_failures=False` to suppress failure file creation

### Configuration Options
- `include_annotations`: Include Zotero highlights/comments (default: True)
- `include_notes`: Include Zotero standalone notes (default: False)  
- `filter_colors`: Filter annotations by highlight color
- `since`: Only sync items modified after timestamp
- `zotero_library_type`: "user" (personal) or "group" library

## Environment Variables
```bash
READWISE_TOKEN       # Readwise API token
ZOTERO_API_KEY       # Zotero API key
ZOTERO_USER_ID       # Zotero user/library ID
LIBRARY_TYPE         # "user" or "group" (optional)
```