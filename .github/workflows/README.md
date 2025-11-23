# GitHub Workflows

This repository uses GitHub Actions for continuous integration and automated releases.

## Workflows

### 🧪 Test Workflow (`test.yaml`)

Runs on every push and pull request to ensure code quality.

**Jobs:**

1. **Test** - Runs on Python 3.12 and 3.13
   - Installs dependencies with uv
   - Runs pytest with coverage
   - Uploads coverage to Codecov

2. **Lint** - Code quality checks
   - Black formatting check
   - Ruff linting
   - MyPy type checking

3. **Build** - Builds the package
   - Creates distribution packages
   - Uploads build artifacts

### 🚀 Release Workflow (`ci.yaml`)

Automatically creates releases when commits are pushed to the `master` branch.

**Process:**

1. Uses Python Semantic Release to determine version bump
2. Updates version in:
   - `pyproject.toml`
   - `zotero2readwise/__init__.py`
   - `CHANGELOG.md`
3. Builds package with `uv build`
4. Publishes to PyPI
5. Creates GitHub release with artifacts

**Secrets Required:**

- `GH_TOKEN` - GitHub Personal Access Token with repo and workflow permissions
- `PYPI_TOKEN` - PyPI API token for publishing packages
- `CODECOV_TOKEN` - (Optional) Codecov token for coverage reports

## Local Testing

To run tests locally before pushing:

```bash
# Install dependencies
uv sync --all-extras

# Run tests
uv run pytest

# Check formatting
uv run black --check .

# Run linting
uv run ruff check .

# Build package
uv build
```

## Semantic Release

This project uses [Python Semantic Release](https://python-semantic-release.readthedocs.io/) for automated versioning based on conventional commits.

**Commit Message Format:**

- `feat:` - New feature (minor version bump)
- `fix:` - Bug fix (patch version bump)
- `BREAKING CHANGE:` - Breaking change (major version bump)
- `docs:` - Documentation changes (no version bump)
- `chore:` - Maintenance tasks (no version bump)

**Example:**

```
feat: add support for group libraries

This adds the ability to sync annotations from Zotero group libraries.

BREAKING CHANGE: The library_type parameter is now required.
```
