# CHANGELOG


## v1.4.0 (2025-11-23)

### Bug Fixes

- Handle authors with single 'name' field and improve annotation type errors
  ([`05ce8ac`](https://github.com/e-alizadeh/Zotero2Readwise/commit/05ce8acf056fbe0c7c33379a7b94f5d7179c36d1))

- Fix KeyError: 'firstName' for institutional authors that use a single 'name' field instead of
  firstName/lastName (e.g., "World Health Organization") - Add explicit handling for 'ink'
  (handwritten) and 'image' (area) annotation types - Improve error messages for unsupported
  annotation types

- Keep 'run' CLI entry point for backward compatibility
  ([`433b23c`](https://github.com/e-alizadeh/Zotero2Readwise/commit/433b23c2ef55021255c3de6a1a7f296ae3caecec))

Add 'zotero2readwise' as new entry point while keeping 'run' alias to avoid breaking existing
  workflows and scripts.

### Chores

- Update uv.lock
  ([`781f7e1`](https://github.com/e-alizadeh/Zotero2Readwise/commit/781f7e170e507f6056a46c018c5a729522502d92))

- Update uv.lock for version 1.3.1
  ([`ed53c9d`](https://github.com/e-alizadeh/Zotero2Readwise/commit/ed53c9d1be84d71397d31666976b2a94e0e34a34))

### Documentation

- Update README with simplified automation workflow
  ([`8107ee6`](https://github.com/e-alizadeh/Zotero2Readwise/commit/8107ee6b3c8985067ba50a8351202a3b6cf5e2b2))

- Remove automation-example.yaml (refer to Zotero2Readwise-Sync repo instead) - Add minimal workflow
  example using uv/uvx to main README - Revert workflows/README.md to original (CI/release docs
  only)

### Features

- Add CLI improvements and example automation workflow
  ([`d6ad247`](https://github.com/e-alizadeh/Zotero2Readwise/commit/d6ad247be36b71cb0ea327606826cb3539ca57e9))

- Rename CLI entry point from 'run' to 'zotero2readwise' for clarity - Support environment variables
  for credentials (READWISE_TOKEN, ZOTERO_KEY, ZOTERO_LIBRARY_ID, ZOTERO_LIBRARY_TYPE) - Add example
  GitHub Actions workflow using uv and uvx for simple automation - Update workflows README with
  automation setup instructions

The new workflow is much simpler: - No checkout needed - Uses `uvx zotero2readwise` for one-line
  execution - Credentials via env vars (more secure than CLI args)

- Add custom_tag and annotation sorting features (#21, #75)
  ([`5b5000e`](https://github.com/e-alizadeh/Zotero2Readwise/commit/5b5000e3b72ee111cfefcba264d97062548d855d))

- Add --custom_tag CLI argument to prepend a tag to all highlights - Sort annotations by document
  title and annotationSortIndex for proper reading order in Readwise - Add sort_index field to
  ZoteroItem to store Zotero's annotationSortIndex


## v1.3.1 (2025-11-22)

### Bug Fixes

- Resolve issues #82, #44, and #72
  ([`903bf74`](https://github.com/e-alizadeh/Zotero2Readwise/commit/903bf74d8b2ee3ca8e0b0689922043d5bdc694e5))

- Fix #82: Handle empty/invalid JSON responses in Readwise API calls - Gracefully handle empty
  response bodies instead of crashing - Capture raw response text for debugging invalid JSON

- Fix #44: Improve error reporting for failed items - Replace bare except blocks with Exception
  handling - Add error_type and error_message to failed items for debugging - Print warnings when
  items fail to format or convert

- Address #72: Add sample automation workflow - Create automation-example.yaml for users to set up
  scheduled syncs - Include proper secret quoting to avoid shell interpretation issues - Add
  workflow_dispatch for manual triggering

Also includes code style fixes from pre-commit hooks.

### Documentation

- Move automation workflow example to README.md
  ([`aae821d`](https://github.com/e-alizadeh/Zotero2Readwise/commit/aae821d2d5c562940e4481164d3c46b80e20b80e))

- Remove separate automation-example.yaml file - Add GitHub Actions workflow example directly in
  README - Include setup instructions and required secrets - Reference issue #72 for secret quoting
  requirement

- Remove custom workflow section from README
  ([`0ab4604`](https://github.com/e-alizadeh/Zotero2Readwise/commit/0ab460453cb03d2b4c30eb9515c7107e937decf3))


## v1.3.0 (2025-11-05)

### Bug Fixes

- Ensure all workflow commands use proper uv run syntax
  ([`5452ce9`](https://github.com/e-alizadeh/Zotero2Readwise/commit/5452ce980d063aaf451150deb538bae3b57ffeb2))

The black command was failing because the run commands weren't properly using the uv environment.
  Changed all multiline run blocks to single-line commands to ensure proper execution context.

Changes: - Simplified all 'run:' blocks to single-line format - Ensures 'uv run' prefix is correctly
  applied to all tool commands - Affects: black, ruff, mypy, pytest, and uv build commands

This fixes the error: error: Failed to spawn: `black`

Caused by: No such file or directory (os error 2)

- Use uv python install for proper Python environment setup in workflows
  ([`5f03816`](https://github.com/e-alizadeh/Zotero2Readwise/commit/5f03816dfcda7bb2cd243e88aed600e518756ca3))

The previous approach was causing 'black not found' errors because actions/setup-python was setting
  up Python independently of uv, causing a mismatch in the environment.

Key changes: - Remove actions/setup-python@v5 step - Use 'uv python install' to let uv manage Python
  installation - Move setup-uv step before Python setup - Add cache-dependency-glob for better
  caching with uv.lock - This ensures uv has full control over the Python environment

This approach follows uv's recommended GitHub Actions integration:
  https://docs.astral.sh/uv/guides/integration/github/

Benefits: - Ensures Python and dependencies are in sync - uv run commands work correctly - All tools
  (black, ruff, mypy, pytest) are found in the proper venv - Better cache performance with uv.lock
  tracking

- **GitHub Actions**: :bug: resolve pre-commit checks
  ([`c8b12b7`](https://github.com/e-alizadeh/Zotero2Readwise/commit/c8b12b7d36bf9c68bacf46f26103bde3109cdcb8))

- **release**: Resolve semantic-release build failure and version detection
  ([`95b3563`](https://github.com/e-alizadeh/Zotero2Readwise/commit/95b356335452a15adf30ba28c16bae06204eb8bd))

Fix two critical issues preventing successful releases:

## Issue 1: 'uv: command not found' during semantic-release **Root Cause:** python-semantic-release
  action runs in its own Docker container which doesn't have access to uv installed in previous
  workflow steps.

**Solution:** - Changed build_command from 'uv build' to an echo statement - Semantic-release now
  only handles version bumping and tagging - Actual package build happens AFTER semantic-release
  completes - This way uv is available in the workflow environment for building

## Issue 2: Wrong version detection (0.1.0 instead of 1.3.0) **Root Cause:** Tag format mismatch -
  existing tags use 'v' prefix (v1.2.0, v1.1.0) but semantic-release was configured for plain
  version (1.2.0).

**Solution:** - Changed tag_format from '{version}' to 'v{version}' - Now matches existing tag
  pattern in repository - Semantic-release will correctly detect v1.2.0 as current version - Next
  release will be v1.3.0 (for feat) or v1.2.1 (for fix)

## Additional Improvements: - Added commit_parser_options for explicit version bump rules - Enhanced
  build step to show version being built - Added PATH environment to semantic-release step - Better
  logging with 'ls -lh dist/' after build

These changes ensure semantic-release can: 1. Correctly detect the current version from tags 2.
  Calculate the next version based on commits 3. Skip the build step (which requires uv) 4. Let the
  workflow build the package after versioning is complete

### Chores

- Update GitHub workflows for uv and Python 3.12+
  ([`733b80b`](https://github.com/e-alizadeh/Zotero2Readwise/commit/733b80bbb24fbd46af342acda6efbca547accf6a))

## Workflow Updates

### New Test Workflow (`test.yaml`) - Runs on every push and PR for continuous integration -
  Multi-Python version testing (3.12 and 3.13) - Three parallel jobs: - **Test**: Runs pytest with
  coverage on both Python versions - **Lint**: Code quality checks (black, ruff, mypy) - **Build**:
  Validates package building with uv - Uploads coverage reports to Codecov - Uploads build artifacts
  for verification

### Updated Release Workflow (`ci.yaml`) - Migrated from Poetry to uv for dependency management -
  Updated Python version: 3.8 → 3.12 - Uses latest action versions: - actions/checkout@v4 -
  actions/setup-python@v5 - astral-sh/setup-uv@v4 - python-semantic-release@v9.15.1 - Build command
  updated: `poetry build` → `uv build` - Improved semantic release output logging

### Semantic Release Configuration - Updated for python-semantic-release v9 compatibility -
  Configured `version_toml` for new pyproject.toml format - Set build command to `uv build` - Added
  branch matching for main/master - Configured changelog generation

### Documentation - Added `.github/workflows/README.md` with: - Workflow descriptions and job
  details - Required secrets documentation - Local testing instructions - Semantic versioning commit
  format guide

## Breaking Changes - Workflows now require Python 3.12+ (previously 3.8+) - Uses uv instead of
  Poetry for package building

## Migration Notes - No changes needed to existing secrets (GH_TOKEN, PYPI_TOKEN) - Workflows will
  automatically use uv when triggered - All semantic-release functionality preserved

### Code Style

- :art: run pre-commit
  ([`62f57a4`](https://github.com/e-alizadeh/Zotero2Readwise/commit/62f57a4779d97167fed6af87026f942dc8023a46))

### Features

- Migrate from Poetry to uv, upgrade to Python 3.12+, add comprehensive tests, fix Unicode issue #90
  ([`f606e12`](https://github.com/e-alizadeh/Zotero2Readwise/commit/f606e1294779107a8e6731a5c63942089f743f5e))

## Major Changes

### 1. Migration from Poetry to uv - Replace Poetry with uv for modern Python dependency management
  - Update minimum Python version to 3.12 - Convert pyproject.toml to standard PEP 621 format -
  Generate uv.lock file for reproducible builds - Remove poetry.lock

### 2. Comprehensive Test Suite (86% coverage) - Add pytest-based test suite with 77 tests - Test
  all modules: helper, exception, zotero, readwise, zt2rw - Implement fixtures and mocks for
  isolated testing - Configure pytest with coverage reporting

### 3. Fix Issue #90 - Unicode Character Encoding - Add `ensure_ascii=False` to all json.dump()
  calls in: - zotero.py: save_failed_items_to_json() - readwise.py: save_failed_items_to_json() and
  error logging - Add `encoding="utf-8"` to all file open() operations - Properly handle Chinese
  characters and other non-ASCII Unicode text - Add specific tests for Unicode handling

### 4. Development Environment Updates - Update .pre-commit-config.yaml for Python 3.12 and latest
  hook versions - Update CLAUDE.md with uv setup and testing instructions - Update README.md with uv
  installation and development instructions - Configure pyproject.toml with pytest, coverage, and
  linting tools

### 5. Code Quality Improvements - Target Python 3.12 in black, mypy, and ruff configurations -
  Update dependency versions for Python 3.12+ compatibility - Maintain backward compatibility with
  existing API

## Test Results - 77 tests, all passing - 86% code coverage - Tests include Unicode handling
  validation

## Breaking Changes - Minimum Python version is now 3.12 (previously 3.8) - Poetry is replaced with
  uv (developers need to install uv)

## Migration Guide For developers: ```bash # Install uv curl -LsSf https://astral.sh/uv/install.sh |
  sh

# Install dependencies uv sync --all-extras

# Run tests uv run pytest ```

Resolves: #90


## v1.2.0 (2025-06-20)

### Features

- ✨ add tag filtering functionality with conflict resolution
  ([`7ce4cb7`](https://github.com/e-alizadeh/Zotero2Readwise/commit/7ce4cb7b7faec9c66ba741644cffc8acf9a79e8d))

- Merged PR #80 tag filtering with master branch write_failures - Added --filter_tags and
  --include_filter_tags command line options - Enhanced ZoteroAnnotationsNotes with tag-based
  filtering logic - Fixed author list formatting bug from PR #80 - Applied code formatting with
  black and ruff - All functionality preserved and working correctly


## v1.1.0 (2025-06-20)

### Bug Fixes

- Add python-dotenv dependency and integration test
  ([`5dd4cea`](https://github.com/e-alizadeh/Zotero2Readwise/commit/5dd4cea541dc8c17cb50a01488b6946b849c100f))

### Features

- Add Nix support and suppress_failures option
  ([`d24eaf8`](https://github.com/e-alizadeh/Zotero2Readwise/commit/d24eaf89edfeac557c878933b8d9be56d60332b5))

- Add Nix flake support for installation-free usage - Add --suppress_failures CLI flag to control
  error file creation - Add Python 3.12 compatibility with setuptools dependency - Add
  cross-platform directory handling for read-only environments - Refactor run.py with main()
  function and Poetry script entry point

Implements all changes from PR #81

Co-authored-by: JJJHolscher <jjjholscher@users.noreply.github.com>


## v1.0.0 (2025-06-20)

### Bug Fixes

- Correct author list formatting
  ([`1eac8d6`](https://github.com/e-alizadeh/Zotero2Readwise/commit/1eac8d6d052667130ef4586c509f84d026293ee3))

- Lock file out of date with pyproject.toml
  ([`a60461e`](https://github.com/e-alizadeh/Zotero2Readwise/commit/a60461e25591dc0f9bac09d9c275e6fc2ca93fb9))

- Regenerate poetry.lock file to match pyproject.toml
  ([`4726a91`](https://github.com/e-alizadeh/Zotero2Readwise/commit/4726a917424d6b468d70baa057d5ca9393bd6c48))

- **GHA**: Update CI workflow to install project root with Poetry
  ([`feed4d9`](https://github.com/e-alizadeh/Zotero2Readwise/commit/feed4d90aa8f355c3abb838965051e09ba81311f))

- **GHA**: Update CI workflow to use `snok/install-poetry` action for installation
  ([`b436875`](https://github.com/e-alizadeh/Zotero2Readwise/commit/b436875df55412086361edf6d7330f796a23281d))

### Features

- Allow filtering by tag
  ([`438ced8`](https://github.com/e-alizadeh/Zotero2Readwise/commit/438ced8b4c5bd58b4db153f2c3f660524de89c49))

### Refactoring

- Exclude filter tags from annotations by default
  ([`9fd6a93`](https://github.com/e-alizadeh/Zotero2Readwise/commit/9fd6a9318be4663f8313e4c8c915216c6a761b0f))


## v0.4.5 (2024-02-22)

### Bug Fixes

- :memo: update an oversight in the help
  ([`ef9ad94`](https://github.com/e-alizadeh/Zotero2Readwise/commit/ef9ad946941a0c1be5d769a263e35cb3f7c3aba6))

- Empty commit to build a new release for PR#77
  ([`7375368`](https://github.com/e-alizadeh/Zotero2Readwise/commit/7375368afd4657eda37b6662bc1f12bc07018aab))

### Build System

- :construction_worker: add `zotero2readwise` as a package to `pyproject.toml`.
  ([`d45c77d`](https://github.com/e-alizadeh/Zotero2Readwise/commit/d45c77da04f4fd367021e88abb1bc7bb2dc81c95))

Update pre-commit


## v0.4.4 (2023-12-12)

### Bug Fixes

- Merge pull request #71 from jmhammond/master
  ([`45a79f7`](https://github.com/e-alizadeh/Zotero2Readwise/commit/45a79f74c1eb1490cf15af29d98ff9a1f0b7bfd1))

Fixes key error in metadata and ignores ink


## v0.4.3 (2023-11-27)

### Bug Fixes

- :ambulance: use library path import instead of local one
  ([`b00d2da`](https://github.com/e-alizadeh/Zotero2Readwise/commit/b00d2da8fefc1e5bb14aed0d11fa99bcc58cb896))


## v0.4.2 (2023-11-16)

### Bug Fixes

- Add `len`
  ([`59d3fad`](https://github.com/e-alizadeh/Zotero2Readwise/commit/59d3fadfe6a730deb86f76df486fcf54d3138aab))


## v0.4.1 (2023-11-08)

### Bug Fixes

- **pyproject**: Version bump config
  ([`566989b`](https://github.com/e-alizadeh/Zotero2Readwise/commit/566989be781ba7a7062e500ada646918c6d2e60a))


## v0.4.0 (2023-11-08)

### Features

- **since**: Finish functionallity
  ([`349eaa6`](https://github.com/e-alizadeh/Zotero2Readwise/commit/349eaa6a6570e85ee6aea6121a8988f0c9d392e0))

- get_all_zotero_items use since - refactor: retrieve_all_* to one function with item_type as
  parameter

- **since**: Only sync since last sync
  ([`42b3449`](https://github.com/e-alizadeh/Zotero2Readwise/commit/42b3449d93f69f759c54a5bcb3ac82e18b463f19))

Storing the last synchronization timestamp in a file allows for incremental syncing, efficiently
  updating only the new highlights since the last sync, ideal for large collections.


## v0.3.4 (2023-11-07)

### Bug Fixes

- Versions and update GH Token secret
  ([`073a57d`](https://github.com/e-alizadeh/Zotero2Readwise/commit/073a57d4f62c6a36bb4907cedee6c52c237b84eb))


## v0.3.3 (2023-11-07)

### Bug Fixes

- Use more distinct step id for GHA step
  ([`5d30a25`](https://github.com/e-alizadeh/Zotero2Readwise/commit/5d30a2536c5046e4f175507fd5d68a86d1f2c264))


## v0.3.2 (2023-11-07)

### Bug Fixes

- Minor changes to release a new pkg after merging
  ([`7b94b33`](https://github.com/e-alizadeh/Zotero2Readwise/commit/7b94b33e97d7ee6481fb357006c818504f6da2e4))

### Refactoring

- Remove unrelated branches
  ([`767c598`](https://github.com/e-alizadeh/Zotero2Readwise/commit/767c598c4e1dc6ba72aa604cb59ca3085a86aaea))


## v0.3.1 (2023-11-06)

### Bug Fixes

- Check of max_length first
  ([`5d69300`](https://github.com/e-alizadeh/Zotero2Readwise/commit/5d693001a84413510c451a6e0f6841197f0dd64b))

Only truncate if needed. Make code more readable.

- Creator/author field
  ([`3053550`](https://github.com/e-alizadeh/Zotero2Readwise/commit/305355066773e2009f2c865cc53fee56d2dd9211))

If there are more than three authors, replace the rest with "et al."

- Enusuring backward compatibility
  ([`0d5197c`](https://github.com/e-alizadeh/Zotero2Readwise/commit/0d5197ce1f648945bdfebf109d98f4c350f8166b))

To prevent the occurrence of duplicate entries in Readwise, we will amend the authors' names to 'et
  al.' exclusively in instances where their works have not been previously imported.

- Latest correct version. add debugging printouts
  ([`9089fe1`](https://github.com/e-alizadeh/Zotero2Readwise/commit/9089fe1adfe738ceffa6e9f6750feb62695c57be))

- Semantic release configs in pyproject.toml
  ([`50a844d`](https://github.com/e-alizadeh/Zotero2Readwise/commit/50a844d282dbb3fb773977cc0810354794c10c9a))

- Test a patch release
  ([`8ebb3c8`](https://github.com/e-alizadeh/Zotero2Readwise/commit/8ebb3c8f279e5d74ca57e691e154c702abd8af5f))

- **gha**: Try another fix for workflow
  ([`cb2f88f`](https://github.com/e-alizadeh/Zotero2Readwise/commit/cb2f88f8c295bcdfb926089e798c1f71467c288b))

- **gha**: Update the workflow for package release
  ([`b6cbda7`](https://github.com/e-alizadeh/Zotero2Readwise/commit/b6cbda71e79d4a75fcd507611e9507c01327962b))

### Refactoring

- Change if condition in the GHA.
  ([`ff27c6f`](https://github.com/e-alizadeh/Zotero2Readwise/commit/ff27c6fb0760025a97434e7f16d808ef32f8798e))


## v0.3.0 (2023-10-10)

### Bug Fixes

- Manual tagging
  ([`c2ae640`](https://github.com/e-alizadeh/Zotero2Readwise/commit/c2ae6404ecc5384b206e5b1e0b14d350a2e7661a))


## v0.2.7 (2023-10-10)

### Bug Fixes

- Empty
  ([`5ad6394`](https://github.com/e-alizadeh/Zotero2Readwise/commit/5ad6394b6cec88e3fd9801206abd87ad6f7dfab4))

- Empty commit
  ([`53db8e0`](https://github.com/e-alizadeh/Zotero2Readwise/commit/53db8e0fa14e06df4c8f4f9bf276d9d32d0c34cf))

- Python semantic release repo name
  ([`236d47c`](https://github.com/e-alizadeh/Zotero2Readwise/commit/236d47c096e2bc6d2c5c83208277ee72d02acc8c))

### Build System

- **GitHub Actions**: :building_construction: pinpoint semantic releaset GH Action
  ([`fb5f6cf`](https://github.com/e-alizadeh/Zotero2Readwise/commit/fb5f6cf644c19d51a9c90f1df54820ae7abc1c92))

### Chores

- :see_no_evil: update `.gitignore`
  ([`9efe4f5`](https://github.com/e-alizadeh/Zotero2Readwise/commit/9efe4f5375675f2be52bde3831e1c6f0b0be0d82))

### Features

- Empty commit to trigger release build
  ([`7c7577c`](https://github.com/e-alizadeh/Zotero2Readwise/commit/7c7577c0e16dbc86e47f8906d0b8ca80168b185f))

- Merge pull request #47 from noeleont/feat/filter-color
  ([`c6af8b2`](https://github.com/e-alizadeh/Zotero2Readwise/commit/c6af8b2d16cffe46e29e985bc77f24a4b3401799))

Add color filter support

### Refactoring

- **GitHub Actions**: :building_construction: release after merging to master
  ([`412988f`](https://github.com/e-alizadeh/Zotero2Readwise/commit/412988f4b07f424f7e25802818f852e413b10b34))


## v0.2.6 (2022-10-31)

### Bug Fixes

- Adding spaces
  ([`e73352d`](https://github.com/e-alizadeh/Zotero2Readwise/commit/e73352d7ca7de9aa60c22958e2ce55ff35ba26e7))

- Empty commit for new release
  ([`7fa1b2b`](https://github.com/e-alizadeh/Zotero2Readwise/commit/7fa1b2beca4d41b5dfdabc753766cf82a9eaccba))

- Empty commit for new release
  ([`c1038c3`](https://github.com/e-alizadeh/Zotero2Readwise/commit/c1038c34a4880373b60254161df734443ed9c049))

- Empty commit for new release
  ([`65e2f44`](https://github.com/e-alizadeh/Zotero2Readwise/commit/65e2f444dfab59dd6704404d18e9742d0d591a4d))

### Chores

- Ignore json files
  ([`42319cb`](https://github.com/e-alizadeh/Zotero2Readwise/commit/42319cb1c69a89861784871e8488709df594dbe9))

### Refactoring

- Update failed directory path. Indent the output json files for cleaner output.
  ([`8cfee3d`](https://github.com/e-alizadeh/Zotero2Readwise/commit/8cfee3dd28e3fb008236aa56ce66dff34c77bc75))


## v0.2.5 (2022-10-19)

### Bug Fixes

- Merge pull request #28 from stefanku/master
  ([`ea16ffa`](https://github.com/e-alizadeh/Zotero2Readwise/commit/ea16ffaf1c911b693095e68773771a7ac408fc4f))

Update zotero.py


## v0.2.4 (2022-04-24)

### Bug Fixes

- Remove category from Readwise source_url
  ([`0ed6118`](https://github.com/e-alizadeh/Zotero2Readwise/commit/0ed61182b935af8fd28e7fd0867b048163a69550))

- Update iPython to resolve a security bug.
  ([`12b1908`](https://github.com/e-alizadeh/Zotero2Readwise/commit/12b19084154e4ecaebd5d5e3d05d6fd0c68b0996))


## v0.2.3 (2022-01-07)

### Bug Fixes

- Use alternate link Zotero (`https://www.zotero.org/username/items/<itemKey>`) that has a html
  content instead of self link (`https://api.zotero.org/users/<userID>/items/<itemKey>`) that
  contains a JSON content and calls the API.
  ([`3310ad1`](https://github.com/e-alizadeh/Zotero2Readwise/commit/3310ad130afdcc977a8eb771712950d0d70064d1))


## v0.2.2 (2022-01-03)

### Bug Fixes

- An oversight in `Zotero2Readwise` class method `run()` (previously `run_all())`
  ([`e2b1336`](https://github.com/e-alizadeh/Zotero2Readwise/commit/e2b133634372b44cefc728923ae7ef384c69adda))


## v0.2.1 (2022-01-03)

### Bug Fixes

- Get non-empty objects from ZoteroItem (so that we have a JSON serializable object)
  ([`6b79fc9`](https://github.com/e-alizadeh/Zotero2Readwise/commit/6b79fc9bf457acd78287a8f0cbe1800f335e52fc))

- Ignore highlights more than 8191 characters (readwise limit for a highlight.)
  ([`7503324`](https://github.com/e-alizadeh/Zotero2Readwise/commit/7503324150d50db72abd3c3cbfda8b469a7d596d))

### Documentation

- Define Zotero2ReadwiseError exception object.
  ([`7d5022a`](https://github.com/e-alizadeh/Zotero2Readwise/commit/7d5022a0ebc28e170e07dc004042981b2be7e314))

- Improve printouts for both Zotero and Readwise operations
  ([`5a22717`](https://github.com/e-alizadeh/Zotero2Readwise/commit/5a22717987a509c123b233dfd33aeded1a9902cd))


## v0.2.0 (2022-01-01)

### Bug Fixes

- Remove filtering zotero items upto 5 items.
  ([`4f3e5e0`](https://github.com/e-alizadeh/Zotero2Readwise/commit/4f3e5e097ec9f6b99e709c1b3be306802a672023))

### Features

- Refactor `Zotero2Readwise.run()` to pass a custom number of Zotero annotations and notes instead
  of running all.
  ([`7c8a337`](https://github.com/e-alizadeh/Zotero2Readwise/commit/7c8a3372b642e3056c5279dcfa06470eb6981f34))


## v0.1.1 (2022-01-01)

### Bug Fixes

- Project details
  ([`502806c`](https://github.com/e-alizadeh/Zotero2Readwise/commit/502806cceb8f03a8bc2ae2d3f6d79a202d7e9452))


## v0.1.0 (2022-01-01)

### Documentation

- Add instructions to README.
  ([`925ecf9`](https://github.com/e-alizadeh/Zotero2Readwise/commit/925ecf9d3283d8c07faa5b05c5e04ae89164622a))

### Features

- Add `ZoteroAnnotationsNotes` to `Readwise` object.
  ([`8f34989`](https://github.com/e-alizadeh/Zotero2Readwise/commit/8f349894c2a65dc3a0df5e60a1fd2ec32047f72f))

- Define ReadwiseAPI and ReadwiseHighlight dataclasses.
  ([`8d5488f`](https://github.com/e-alizadeh/Zotero2Readwise/commit/8d5488f0c8cfbe5f4897c59c7e251ac10203c7c7))

- Define Zotero2Readwise class that runs everything.
  ([`8361426`](https://github.com/e-alizadeh/Zotero2Readwise/commit/8361426d8c321162333fb44432f76cefb310e231))

- Define ZoteroAnnotationsNotes. Add `sanitize_tag()` helper function.
  ([`d5f27d6`](https://github.com/e-alizadeh/Zotero2Readwise/commit/d5f27d602a9b44d38b0c13974bb4acd73f2bc915))

Comment out ZoteroAnnotation dataclass.

- Define ZoteroItem dataclass and use that to format the zotero annotations (separate formatting
  from Readwise class).
  ([`cfa1b12`](https://github.com/e-alizadeh/Zotero2Readwise/commit/cfa1b1277d7dcae15c687a96aac86115b1e7e4d8))

- Functions to retrieve all annotations and notes from Zotero.
  ([`cafb998`](https://github.com/e-alizadeh/Zotero2Readwise/commit/cafb9982827c5f85ddb0a6c65ec21f2e21747b00))

- Major changes to Readwise class.
  ([`ea27b8c`](https://github.com/e-alizadeh/Zotero2Readwise/commit/ea27b8c0004f6618803452a2df33d7af26a054eb))

- Save failed items to a json file. Add printouts.
  ([`e107fc0`](https://github.com/e-alizadeh/Zotero2Readwise/commit/e107fc0434b75d021c12674556d83e0df9947649))
