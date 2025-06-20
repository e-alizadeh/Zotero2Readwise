# CHANGELOG



## v0.4.5 (2024-02-22)

### Build

* build: :construction_worker: add `zotero2readwise` as a package to `pyproject.toml`.

Update pre-commit ([`d45c77d`](https://github.com/e-alizadeh/Zotero2Readwise/commit/d45c77da04f4fd367021e88abb1bc7bb2dc81c95))

### Fix

* fix: :memo: update an oversight in the help ([`ef9ad94`](https://github.com/e-alizadeh/Zotero2Readwise/commit/ef9ad946941a0c1be5d769a263e35cb3f7c3aba6))

* fix: empty commit to build a new release for PR#77 ([`7375368`](https://github.com/e-alizadeh/Zotero2Readwise/commit/7375368afd4657eda37b6662bc1f12bc07018aab))

### Unknown

* Merge pull request #79 from e-alizadeh/74-runpy-h-says-notes-are-included-by-default-by-they-arent

fix: :memo: update an oversight in the help ([`bd9a2dc`](https://github.com/e-alizadeh/Zotero2Readwise/commit/bd9a2dc279b1992bffc14d710f2aea92ad692cab))

* Merge pull request #78 from e-alizadeh/update-library-pkg

fix: empty commit to build a new release for PR#77 ([`54d38ac`](https://github.com/e-alizadeh/Zotero2Readwise/commit/54d38acaa9a53e839ae1accce5e948fe58f43b2d))

* Merge pull request #77 from e-alizadeh/update-library-pkg

build: :construction_worker: add `zotero2readwise` as a package to `pyproject.toml`. ([`2e0601d`](https://github.com/e-alizadeh/Zotero2Readwise/commit/2e0601d58950e23c220ce45bfc539016b5ed4947))


## v0.4.4 (2023-12-12)

### Fix

* fix: Merge pull request #71 from jmhammond/master

Fixes key error in metadata and ignores ink ([`45a79f7`](https://github.com/e-alizadeh/Zotero2Readwise/commit/45a79f74c1eb1490cf15af29d98ff9a1f0b7bfd1))

### Unknown

* Fixes key error in metadata and ignores ink

This implements default values for metadata keys used elsewhere in code (avoiding key errors)

It also raises an exception for ink annotations for handwritten notes, effectively ignoring them. ([`391eb7a`](https://github.com/e-alizadeh/Zotero2Readwise/commit/391eb7a96bf5fa054a3f33fba7eaa687bfcc34fd))


## v0.4.3 (2023-11-27)

### Fix

* fix: :ambulance: use library path import instead of local one ([`b00d2da`](https://github.com/e-alizadeh/Zotero2Readwise/commit/b00d2da8fefc1e5bb14aed0d11fa99bcc58cb896))

### Unknown

* Merge pull request #67 from e-alizadeh/fix/local-import-from-helper

fix: :ambulance: use library path import instead of local one ([`bfc5f15`](https://github.com/e-alizadeh/Zotero2Readwise/commit/bfc5f1514625da94799672bd48b9025ec5e8a633))


## v0.4.2 (2023-11-16)

### Fix

* fix: add `len` ([`59d3fad`](https://github.com/e-alizadeh/Zotero2Readwise/commit/59d3fadfe6a730deb86f76df486fcf54d3138aab))

* fix: check of max_length first

Only truncate if needed. Make code more readable. ([`5d69300`](https://github.com/e-alizadeh/Zotero2Readwise/commit/5d693001a84413510c451a6e0f6841197f0dd64b))

### Unknown

* Merge pull request #60 from noeleont/fix/author_names

fix: creator/author field

Thanks @noeleont for the contribution. ([`c5b7c59`](https://github.com/e-alizadeh/Zotero2Readwise/commit/c5b7c5940d7672fbb4b384917fe022635e30e88e))

* Merge branch &#39;e-alizadeh:master&#39; into fix/author_names ([`603cdb4`](https://github.com/e-alizadeh/Zotero2Readwise/commit/603cdb4e856969e44b5cdec2f82616fac9f55e01))


## v0.4.1 (2023-11-08)

### Fix

* fix(pyproject): version bump config ([`566989b`](https://github.com/e-alizadeh/Zotero2Readwise/commit/566989be781ba7a7062e500ada646918c6d2e60a))

### Unknown

* Merge pull request #65 from e-alizadeh/fix-semantic-release-bumpversion

fix(pyproject): version bump config ([`04f1083`](https://github.com/e-alizadeh/Zotero2Readwise/commit/04f10837cd62417c3bff89fadd9c5cc1516374f2))


## v0.4.0 (2023-11-08)

### Fix

* fix: enusuring backward compatibility

To prevent the occurrence of duplicate entries in Readwise, we will
amend the authors&#39; names to &#39;et al.&#39; exclusively in instances where
their works have not been previously imported. ([`0d5197c`](https://github.com/e-alizadeh/Zotero2Readwise/commit/0d5197ce1f648945bdfebf109d98f4c350f8166b))

### Unknown

* Merge pull request #59 from noeleont/master

Add --use_since feature flag ([`3e204d2`](https://github.com/e-alizadeh/Zotero2Readwise/commit/3e204d2863bc5aee64119fe4288af33715611245))


## v0.3.4 (2023-11-07)

### Fix

* fix: versions and update GH Token secret ([`073a57d`](https://github.com/e-alizadeh/Zotero2Readwise/commit/073a57d4f62c6a36bb4907cedee6c52c237b84eb))

### Unknown

* Merge pull request #64 from e-alizadeh:update-gh-token

fix: versions and update GH Token secret ([`b8c377c`](https://github.com/e-alizadeh/Zotero2Readwise/commit/b8c377c6e6b5cab1c53935b6dd6fa10a7b6c811f))


## v0.3.3 (2023-11-07)

### Fix

* fix: use more distinct step id for GHA step ([`5d30a25`](https://github.com/e-alizadeh/Zotero2Readwise/commit/5d30a2536c5046e4f175507fd5d68a86d1f2c264))

### Unknown

* Merge pull request #63 from e-alizadeh:fix/semantic-release

fix: use more distinct step id for GHA step ([`9602a0f`](https://github.com/e-alizadeh/Zotero2Readwise/commit/9602a0fabe88e574d33c0ec69cafc3fb23914f6d))


## v0.3.2 (2023-11-07)

### Fix

* fix: minor changes to release a new pkg after merging ([`7b94b33`](https://github.com/e-alizadeh/Zotero2Readwise/commit/7b94b33e97d7ee6481fb357006c818504f6da2e4))

### Refactor

* refactor: remove unrelated branches ([`767c598`](https://github.com/e-alizadeh/Zotero2Readwise/commit/767c598c4e1dc6ba72aa604cb59ca3085a86aaea))

### Unknown

* Merge pull request #62 from e-alizadeh/new-release

fix: minor changes to release a new pkg after merging ([`4944d94`](https://github.com/e-alizadeh/Zotero2Readwise/commit/4944d941c654a9f3d7e99b657f8b80a74c4d3ee3))

* Merge pull request #61 from e-alizadeh/fix/github-action-pkg-release

Fix/GitHub action pkg release ([`c89e8c1`](https://github.com/e-alizadeh/Zotero2Readwise/commit/c89e8c14c74fad1d6d7aaf4af17ed30bc6120af2))


## v0.3.1 (2023-11-07)

### Feature

* feat(since): finish functionallity

- get_all_zotero_items use since
- refactor: retrieve_all_* to one function with item_type as parameter ([`349eaa6`](https://github.com/e-alizadeh/Zotero2Readwise/commit/349eaa6a6570e85ee6aea6121a8988f0c9d392e0))

* feat(since): only sync since last sync

Storing the last synchronization timestamp in a file allows for
incremental syncing, efficiently updating only the new highlights
since the last sync, ideal for large collections. ([`42b3449`](https://github.com/e-alizadeh/Zotero2Readwise/commit/42b3449d93f69f759c54a5bcb3ac82e18b463f19))

### Fix

* fix: semantic release configs in pyproject.toml ([`50a844d`](https://github.com/e-alizadeh/Zotero2Readwise/commit/50a844d282dbb3fb773977cc0810354794c10c9a))

* fix: latest correct version. add debugging printouts ([`9089fe1`](https://github.com/e-alizadeh/Zotero2Readwise/commit/9089fe1adfe738ceffa6e9f6750feb62695c57be))

* fix: test a patch release ([`8ebb3c8`](https://github.com/e-alizadeh/Zotero2Readwise/commit/8ebb3c8f279e5d74ca57e691e154c702abd8af5f))

* fix(gha): try another fix for workflow ([`cb2f88f`](https://github.com/e-alizadeh/Zotero2Readwise/commit/cb2f88f8c295bcdfb926089e798c1f71467c288b))

* fix(gha): update the workflow for package release ([`b6cbda7`](https://github.com/e-alizadeh/Zotero2Readwise/commit/b6cbda71e79d4a75fcd507611e9507c01327962b))

* fix: creator/author field

If there are more than three authors, replace the rest with &#34;et al.&#34; ([`3053550`](https://github.com/e-alizadeh/Zotero2Readwise/commit/305355066773e2009f2c865cc53fee56d2dd9211))

### Refactor

* refactor: change if condition in the GHA. ([`ff27c6f`](https://github.com/e-alizadeh/Zotero2Readwise/commit/ff27c6fb0760025a97434e7f16d808ef32f8798e))


## v0.3.0 (2023-10-11)

### Fix

* fix: manual tagging ([`c2ae640`](https://github.com/e-alizadeh/Zotero2Readwise/commit/c2ae6404ecc5384b206e5b1e0b14d350a2e7661a))

### Unknown

* Merge pull request #57 from e-alizadeh/test-manual-fix

fix: manual tagging ([`122df24`](https://github.com/e-alizadeh/Zotero2Readwise/commit/122df243d7991160a35af988320a926366658310))

* Merge pull request #56 from e-alizadeh/fix-package-release

Fix package release ([`600fc78`](https://github.com/e-alizadeh/Zotero2Readwise/commit/600fc78263ddced5581e65605ae7584dd6737b4d))


## v0.2.7 (2023-10-11)

### Build

* build(GitHub Actions): :building_construction: pinpoint semantic releaset GH Action ([`fb5f6cf`](https://github.com/e-alizadeh/Zotero2Readwise/commit/fb5f6cf644c19d51a9c90f1df54820ae7abc1c92))

### Chore

* chore: :see_no_evil: update `.gitignore` ([`9efe4f5`](https://github.com/e-alizadeh/Zotero2Readwise/commit/9efe4f5375675f2be52bde3831e1c6f0b0be0d82))

### Feature

* feat: empty commit to trigger release build ([`7c7577c`](https://github.com/e-alizadeh/Zotero2Readwise/commit/7c7577c0e16dbc86e47f8906d0b8ca80168b185f))

* feat: Merge pull request #47 from noeleont/feat/filter-color

Add color filter support ([`c6af8b2`](https://github.com/e-alizadeh/Zotero2Readwise/commit/c6af8b2d16cffe46e29e985bc77f24a4b3401799))

### Fix

* fix: empty ([`5ad6394`](https://github.com/e-alizadeh/Zotero2Readwise/commit/5ad6394b6cec88e3fd9801206abd87ad6f7dfab4))

* fix: empty commit ([`53db8e0`](https://github.com/e-alizadeh/Zotero2Readwise/commit/53db8e0fa14e06df4c8f4f9bf276d9d32d0c34cf))

* fix: python semantic release repo name ([`236d47c`](https://github.com/e-alizadeh/Zotero2Readwise/commit/236d47c096e2bc6d2c5c83208277ee72d02acc8c))

### Refactor

* refactor(GitHub Actions): :building_construction: release after merging to master ([`412988f`](https://github.com/e-alizadeh/Zotero2Readwise/commit/412988f4b07f424f7e25802818f852e413b10b34))

### Unknown

* update gitignore ([`6d59196`](https://github.com/e-alizadeh/Zotero2Readwise/commit/6d5919601c39216f6f25dec47b60fba882c9bbf5))

* Merge pull request #55 from e-alizadeh/fix-package-release

fix: empty commit ([`220e8cb`](https://github.com/e-alizadeh/Zotero2Readwise/commit/220e8cb044c12adfc92abd9be6fb0fbb9da88197))

* Merge pull request #54 from e-alizadeh/fix-package-release

use v7.32.2 semantic release ([`1dc7d21`](https://github.com/e-alizadeh/Zotero2Readwise/commit/1dc7d21283991d772f82ec00752f78c7474a5f3f))

* use v7.32.2 semantic release ([`2cf05bf`](https://github.com/e-alizadeh/Zotero2Readwise/commit/2cf05bf3d6d0ff0dab760cae4d59565da5fffcad))

* Merge pull request #53 from e-alizadeh/fix-package-release

Fix-package-release ([`3a4fbae`](https://github.com/e-alizadeh/Zotero2Readwise/commit/3a4fbaee2ab2281928851f75c7b05c8fd6e38339))

* Merge pull request #52 from e-alizadeh/release

Release ([`4fc31cb`](https://github.com/e-alizadeh/Zotero2Readwise/commit/4fc31cbdf0a584118800e499923da60ae0718b8f))

* Merge pull request #51 from e-alizadeh/master

New release ([`94ac79d`](https://github.com/e-alizadeh/Zotero2Readwise/commit/94ac79daf93e695822d09d12084ee3e8cbdf273b))

* Merge pull request #50 from e-alizadeh/pinpoint-semantic-release

feat: empty commit to trigger release build ([`2462f5f`](https://github.com/e-alizadeh/Zotero2Readwise/commit/2462f5fc1fd3ee7f5f451e5edd8f36d81cc5a5f8))

* Merge pull request #49 from e-alizadeh/pinpoint-semantic-release

Pinpoint semantic release ([`ebcdf43`](https://github.com/e-alizadeh/Zotero2Readwise/commit/ebcdf4308a81ff2be6bd14df34227e5e2d978f37))

* Merge pull request #48 from e-alizadeh/master

Release attachment URL and color support ([`91c8b15`](https://github.com/e-alizadeh/Zotero2Readwise/commit/91c8b1555e90617c0a309de3d49a179f94b7988c))

* Merge pull request #46 from noeleont/feat/attachment_url

Add support for attachment_url ([`c593097`](https://github.com/e-alizadeh/Zotero2Readwise/commit/c593097340af4b7890b77860be1eaab0c1898ba2))

* Add color filter support

This allows a workflow where only certain annotations get imported.

Closes Only sync pre-specified color(s)? #25 ([`5413f9b`](https://github.com/e-alizadeh/Zotero2Readwise/commit/5413f9ba8883ebe6cf11e3de535e9851440ed645))

* Add support for attachment_url

If an attachment is present and is pdf it will be used as highlight_url.

This allows Readwise to open Annotation in Zotero. ([`37d43a4`](https://github.com/e-alizadeh/Zotero2Readwise/commit/37d43a40c01ebc8d92f4b903e7bed1642060c7d8))

* Merge pull request #42 from nobuyukioishi/patch-1

Fix invalid link to Zotero Settings page ([`142f8eb`](https://github.com/e-alizadeh/Zotero2Readwise/commit/142f8eb417da9e365d20ad391b25a3362b932f61))

* Fix invalid link to Zotero Settings page

I changed &#34;https://www.zotero.org/settings/key&#34; to &#34;https://www.zotero.org/settings/keys&#34; to points to the correct page. ([`1d09362`](https://github.com/e-alizadeh/Zotero2Readwise/commit/1d093622ec94279602e12aa55dbc8cbcfc695069))

* add parenthesis ([`d2c1e82`](https://github.com/e-alizadeh/Zotero2Readwise/commit/d2c1e82e627cdbdf0110c3e4b498ccb874d88135))

* [skip ci] Update changelog ([`77681ee`](https://github.com/e-alizadeh/Zotero2Readwise/commit/77681eee58d3ef8e78d6f3213ae84aed38fe783a))

* Merge pull request #39 from e-alizadeh/release

Release ([`5e4d093`](https://github.com/e-alizadeh/Zotero2Readwise/commit/5e4d0937aa06457f86eb854cce7712697acf5fc1))


## v0.2.6 (2022-10-31)

### Chore

* chore: ignore json files ([`42319cb`](https://github.com/e-alizadeh/Zotero2Readwise/commit/42319cb1c69a89861784871e8488709df594dbe9))

### Fix

* fix: adding spaces ([`e73352d`](https://github.com/e-alizadeh/Zotero2Readwise/commit/e73352d7ca7de9aa60c22958e2ce55ff35ba26e7))

* fix: empty commit for new release ([`7fa1b2b`](https://github.com/e-alizadeh/Zotero2Readwise/commit/7fa1b2beca4d41b5dfdabc753766cf82a9eaccba))

* fix: empty commit for new release ([`c1038c3`](https://github.com/e-alizadeh/Zotero2Readwise/commit/c1038c34a4880373b60254161df734443ed9c049))

* fix: empty commit for new release ([`65e2f44`](https://github.com/e-alizadeh/Zotero2Readwise/commit/65e2f444dfab59dd6704404d18e9742d0d591a4d))

### Refactor

* refactor: update failed directory path. Indent the output json files for cleaner output. ([`8cfee3d`](https://github.com/e-alizadeh/Zotero2Readwise/commit/8cfee3dd28e3fb008236aa56ce66dff34c77bc75))

### Unknown

* Merge pull request #38 from e-alizadeh/master

fix: logging ([`e5182a4`](https://github.com/e-alizadeh/Zotero2Readwise/commit/e5182a49afc9407a2e4a8e10ace0382d369005ac))

* Merge pull request #37 from e-alizadeh/new-release

New release ([`5c13829`](https://github.com/e-alizadeh/Zotero2Readwise/commit/5c138297d94a9773ec9aa262bbaff7f6bc72f468))

* Merge pull request #36 from e-alizadeh/master

New release ([`a065c29`](https://github.com/e-alizadeh/Zotero2Readwise/commit/a065c29dff641dba93f49919ee4cdbb50e2775d0))

* Merge pull request #35 from e-alizadeh/new-release

New release ([`9cc7321`](https://github.com/e-alizadeh/Zotero2Readwise/commit/9cc7321187163a16cbf97294d127420b6f459ab9))

* Merge pull request #34 from e-alizadeh/new-release

fix: empty commit for new release ([`36b1e0f`](https://github.com/e-alizadeh/Zotero2Readwise/commit/36b1e0f50103da49a1054b15de174fddc70096c2))

* Merge pull request #33 from e-alizadeh/master

Relase [Better logging #32](https://github.com/e-alizadeh/Zotero2Readwise/pull/32) ([`d86c621`](https://github.com/e-alizadeh/Zotero2Readwise/commit/d86c621f68d23062530d9ec8f26004fbb38c7d1b))

* Merge pull request #32 from e-alizadeh/better-logging

Better logging ([`0788e4c`](https://github.com/e-alizadeh/Zotero2Readwise/commit/0788e4cb36c4049eb9f51c8642a9d87cbae82e3d))

* Merge pull request #30 from e-alizadeh/release

Release ([`79b0eaa`](https://github.com/e-alizadeh/Zotero2Readwise/commit/79b0eaa428d606384ce07abd58bb9e409832eded))


## v0.2.5 (2022-10-19)

### Fix

* fix: Merge pull request #28 from stefanku/master

Update zotero.py ([`ea16ffa`](https://github.com/e-alizadeh/Zotero2Readwise/commit/ea16ffaf1c911b693095e68773771a7ac408fc4f))

### Unknown

* Merge pull request #29 from e-alizadeh/master

fix alternate URL in metadata ([`864cb6c`](https://github.com/e-alizadeh/Zotero2Readwise/commit/864cb6c9ac54f3370ad8bdda1be160dd9856d1d0))

* Update zotero.py ([`991cf7c`](https://github.com/e-alizadeh/Zotero2Readwise/commit/991cf7cc8e761d4f486c28843d18f32adf15772a))

* Merge pull request #26 from floriankilian/patch-1

Update README.md ([`02b36f1`](https://github.com/e-alizadeh/Zotero2Readwise/commit/02b36f18ff86469406fdee8dd9b83888014ba50c))

* Update README.md

Link to Zotero Settings changed from https://www.zotero.org/settings/key to https://www.zotero.org/settings/keys

I also added /new to directly link to generating a new key, maybe you could explain which settings are needed for a new key (read/write). ([`2b2b126`](https://github.com/e-alizadeh/Zotero2Readwise/commit/2b2b126b31b3c01de7e82e7008918447be6f3194))


## v0.2.4 (2022-04-24)

### Fix

* fix: update iPython to resolve a security bug. ([`12b1908`](https://github.com/e-alizadeh/Zotero2Readwise/commit/12b19084154e4ecaebd5d5e3d05d6fd0c68b0996))

* fix: Remove category from Readwise source_url ([`0ed6118`](https://github.com/e-alizadeh/Zotero2Readwise/commit/0ed61182b935af8fd28e7fd0867b048163a69550))

### Unknown

* Merge pull request #24 from e-alizadeh/master

New release ([`543406c`](https://github.com/e-alizadeh/Zotero2Readwise/commit/543406cd6d9b649e621c1b20bad53a437af50999))

* Merge pull request #23 from e-alizadeh/bugfix/update-ipython

fix: update iPython to resolve a security bug. ([`7eacac1`](https://github.com/e-alizadeh/Zotero2Readwise/commit/7eacac15f58e57d9a79cd4d14d4844bb3864ba5d))

* Merge pull request #20 from e-alizadeh/bugfix/source-type

fix: Remove category from Readwise source_url ([`bb30d54`](https://github.com/e-alizadeh/Zotero2Readwise/commit/bb30d540da69b2ea17b041da69ff65b8a5adf8de))

* Update README.md ([`e5fb823`](https://github.com/e-alizadeh/Zotero2Readwise/commit/e5fb823c88c2c4c9d68efb44d6c89a20957b2fb0))

* Update README.md ([`3906450`](https://github.com/e-alizadeh/Zotero2Readwise/commit/3906450f69ee3c298891c7fd67bc643c7108844e))

* Update README.md

Change zt2rw-cronjob to Zotero2Readwise-Sync. 
Fix the GitHub issue link. ([`3b2bc2f`](https://github.com/e-alizadeh/Zotero2Readwise/commit/3b2bc2f8f4a9c5c07f3cb4addb4dc59ba9cc74a5))

* Update README ([`ddf0d64`](https://github.com/e-alizadeh/Zotero2Readwise/commit/ddf0d645382cbb7148cc3b6cc34b5a56067611f3))

* Merge pull request #15 from e-alizadeh/release

Release ([`161e718`](https://github.com/e-alizadeh/Zotero2Readwise/commit/161e7185575319c269db510378d1f5673320d6b1))


## v0.2.3 (2022-01-07)

### Fix

* fix: Use alternate link Zotero (`https://www.zotero.org/username/items/&lt;itemKey&gt;`) that has a html content instead of self link (`https://api.zotero.org/users/&lt;userID&gt;/items/&lt;itemKey&gt;`) that contains a JSON content and calls the API. ([`3310ad1`](https://github.com/e-alizadeh/Zotero2Readwise/commit/3310ad130afdcc977a8eb771712950d0d70064d1))

### Unknown

* Merge pull request #14 from e-alizadeh/master

Fix Readwise highlight url pointing to Zotero API (application/json content type) instead of the link for text/html content type ([`38adbcf`](https://github.com/e-alizadeh/Zotero2Readwise/commit/38adbcf54c7a2a502b7213568c1b85a666f80303))

* Merge pull request #13 from e-alizadeh/bugfix/use-html-link

fix: Use alternate link Zotero (`https://www.zotero.org/username/item… ([`41c1814`](https://github.com/e-alizadeh/Zotero2Readwise/commit/41c1814f5e00023beaeb17ff2db03a9c113095ab))

* Merge branch &#39;release&#39; ([`4cbfb06`](https://github.com/e-alizadeh/Zotero2Readwise/commit/4cbfb064c831a7455aad79d1d6dde17553095ad1))

* Add zt2rw-cronjob to README. ([`284ca1d`](https://github.com/e-alizadeh/Zotero2Readwise/commit/284ca1dddd18f70322e5f5fc1c8650b47d3f50bc))

* Update README.md ([`bdc410e`](https://github.com/e-alizadeh/Zotero2Readwise/commit/bdc410e3e13a9321ac4b4ea0a5a0782da09290e8))

* Update README.md ([`4ec61e3`](https://github.com/e-alizadeh/Zotero2Readwise/commit/4ec61e39a75c45dea92503f0faba8c66c6356ec9))


## v0.2.2 (2022-01-03)

### Fix

* fix: an oversight in `Zotero2Readwise` class method `run()` (previously `run_all())` ([`e2b1336`](https://github.com/e-alizadeh/Zotero2Readwise/commit/e2b133634372b44cefc728923ae7ef384c69adda))

### Unknown

* Merge pull request #11 from e-alizadeh/master

Fix an oversight in running scripts ([`28d3894`](https://github.com/e-alizadeh/Zotero2Readwise/commit/28d389460a9deb48117e17af4e90cd44c2e8590b))

* Merge pull request #10 from e-alizadeh/bugfix/fix-run-argparser

Bugfix/fix run argparser ([`cedfb40`](https://github.com/e-alizadeh/Zotero2Readwise/commit/cedfb405b034de2bab8d6a5e0f41057e631ccc43))


## v0.2.1 (2022-01-03)

### Documentation

* docs: Improve printouts for both Zotero and Readwise operations ([`5a22717`](https://github.com/e-alizadeh/Zotero2Readwise/commit/5a22717987a509c123b233dfd33aeded1a9902cd))

* docs: Define Zotero2ReadwiseError exception object.
Add Zotero2ReadwiseError if POST request to Readwise fails and save the error log to a file. ([`7d5022a`](https://github.com/e-alizadeh/Zotero2Readwise/commit/7d5022a0ebc28e170e07dc004042981b2be7e314))

### Fix

* fix: Get non-empty objects from ZoteroItem (so that we have a JSON serializable object) ([`6b79fc9`](https://github.com/e-alizadeh/Zotero2Readwise/commit/6b79fc9bf457acd78287a8f0cbe1800f335e52fc))

* fix: Ignore highlights more than 8191 characters (readwise limit for a highlight.) ([`7503324`](https://github.com/e-alizadeh/Zotero2Readwise/commit/7503324150d50db72abd3c3cbfda8b469a7d596d))

### Unknown

* Merge pull request #9 from e-alizadeh/master

Bugfix for limited  chars limits in Readwise highlights ([`f27bd0c`](https://github.com/e-alizadeh/Zotero2Readwise/commit/f27bd0cbf25ad68d1ca6d922e118aebec0913d3b))

* Merge pull request #8 from e-alizadeh/bugfix/readwise-text-field-limited-8191-chars

Bugfix/readwise text field limited 8191 chars ([`724f7e5`](https://github.com/e-alizadeh/Zotero2Readwise/commit/724f7e53e362fa5d3f8147d1e243560706d928eb))

* Remove automated saving of failed items.
Update README. ([`07e3612`](https://github.com/e-alizadeh/Zotero2Readwise/commit/07e36124672f24655ecc821a19aa5cab2fd3d6d9))

* Add continue to skip a failed item. ([`476576f`](https://github.com/e-alizadeh/Zotero2Readwise/commit/476576f7ea2e462f2356638e8961785cde51fe35))

* Merge pull request #7 from e-alizadeh/release

Merge back release 0.2.0 ([`5ed3a42`](https://github.com/e-alizadeh/Zotero2Readwise/commit/5ed3a42b22d747f77116e8de28050eb0f66bd5c2))


## v0.2.0 (2022-01-01)

### Feature

* feat: Refactor `Zotero2Readwise.run()` to pass a custom number of Zotero annotations and notes instead of running all.
Rename `run_all()` -&gt; `run()` ([`7c8a337`](https://github.com/e-alizadeh/Zotero2Readwise/commit/7c8a3372b642e3056c5279dcfa06470eb6981f34))

### Fix

* fix: Remove filtering zotero items upto 5 items. ([`4f3e5e0`](https://github.com/e-alizadeh/Zotero2Readwise/commit/4f3e5e097ec9f6b99e709c1b3be306802a672023))

### Unknown

* Merge pull request #6 from e-alizadeh/master

fix: uploading only 5 items! ([`25cd8ec`](https://github.com/e-alizadeh/Zotero2Readwise/commit/25cd8ece896c6bd065cf6b65e14333eef0c7a1e8))

* Update README ([`dc78be3`](https://github.com/e-alizadeh/Zotero2Readwise/commit/dc78be3765a702f827bf0ef962f64748fa056860))

* Update README. ([`759fd8b`](https://github.com/e-alizadeh/Zotero2Readwise/commit/759fd8b3af8ed3015bf9be14e17965703fa510d4))

* Update README ([`4c52024`](https://github.com/e-alizadeh/Zotero2Readwise/commit/4c520247032087f2eb97b91ab07e2274223f3b12))

* Fix a link in the README ([`9bea0d5`](https://github.com/e-alizadeh/Zotero2Readwise/commit/9bea0d50d29956a10ab9e204a24f6bf215dcb1f6))


## v0.1.1 (2022-01-01)

### Fix

* fix: Project details ([`502806c`](https://github.com/e-alizadeh/Zotero2Readwise/commit/502806cceb8f03a8bc2ae2d3f6d79a202d7e9452))

### Unknown

* Merge pull request #5 from e-alizadeh/master

fix: Delete duplicate license entry. ([`21d2514`](https://github.com/e-alizadeh/Zotero2Readwise/commit/21d2514e289dd581d5dfd451419a42407bfd1add))

* Delete duplicate license entry. ([`642f8e1`](https://github.com/e-alizadeh/Zotero2Readwise/commit/642f8e1c152ed3bd2ef86b29215180e2f9cd8c0a))

* Merge pull request #4 from e-alizadeh/master

fix: Project details ([`15871d1`](https://github.com/e-alizadeh/Zotero2Readwise/commit/15871d12d399a5b813940afece80b0ad2952dc15))


## v0.1.0 (2022-01-01)

### Documentation

* docs: Add instructions to README. ([`925ecf9`](https://github.com/e-alizadeh/Zotero2Readwise/commit/925ecf9d3283d8c07faa5b05c5e04ae89164622a))

### Feature

* feat: Define Zotero2Readwise class that runs everything. ([`8361426`](https://github.com/e-alizadeh/Zotero2Readwise/commit/8361426d8c321162333fb44432f76cefb310e231))

* feat: Functions to retrieve all annotations and notes from Zotero.
fix: Get &#34;creators&#34; from metadata. ([`cafb998`](https://github.com/e-alizadeh/Zotero2Readwise/commit/cafb9982827c5f85ddb0a6c65ec21f2e21747b00))

* feat: Major changes to Readwise class.
Update tags and creators signatures of ZoteroItem. ([`ea27b8c`](https://github.com/e-alizadeh/Zotero2Readwise/commit/ea27b8c0004f6618803452a2df33d7af26a054eb))

* feat: Save failed items to a json file. Add printouts. ([`e107fc0`](https://github.com/e-alizadeh/Zotero2Readwise/commit/e107fc0434b75d021c12674556d83e0df9947649))

* feat: Define ZoteroItem dataclass and use that to format the zotero annotations (separate formatting from Readwise class). ([`cfa1b12`](https://github.com/e-alizadeh/Zotero2Readwise/commit/cfa1b1277d7dcae15c687a96aac86115b1e7e4d8))

* feat: Add `ZoteroAnnotationsNotes` to `Readwise` object.
Define `convert_tags_to_readwise_format()`, `format_readwise_note()`, `convert_zotero_annotation_to_readwise_highlight()`

Delete `format_highlights()`. ([`8f34989`](https://github.com/e-alizadeh/Zotero2Readwise/commit/8f349894c2a65dc3a0df5e60a1fd2ec32047f72f))

* feat: Define ZoteroAnnotationsNotes. Add `sanitize_tag()` helper function.

Comment out ZoteroAnnotation dataclass. ([`d5f27d6`](https://github.com/e-alizadeh/Zotero2Readwise/commit/d5f27d602a9b44d38b0c13974bb4acd73f2bc915))

* feat: Define ReadwiseAPI and ReadwiseHighlight dataclasses.
Define Category Enum.
Define Readwise class that post the highlight to Readwise highlight endpoint. ([`8d5488f`](https://github.com/e-alizadeh/Zotero2Readwise/commit/8d5488f0c8cfbe5f4897c59c7e251ac10203c7c7))

### Unknown

* Merge pull request #3 from e-alizadeh/master

Update dir to python version in init. ([`ecad7af`](https://github.com/e-alizadeh/Zotero2Readwise/commit/ecad7af7e3df06eecbc344326c724beb557aaf4b))

* Update dir to python version in init. ([`e510343`](https://github.com/e-alizadeh/Zotero2Readwise/commit/e51034399d06b948e5f737d7bcc56ebfee3b123c))

* Merge pull request #2 from e-alizadeh/master

Update workflow name. ([`d5bab23`](https://github.com/e-alizadeh/Zotero2Readwise/commit/d5bab2360930d9cd09ba017b6d4c8e0127b561a5))

* Update workflow name. ([`35acddb`](https://github.com/e-alizadeh/Zotero2Readwise/commit/35acddb2ca906f8f6e68bd81f2804c545ebd2715))

* Merge pull request #1 from e-alizadeh/master

Update link in README. ([`377669a`](https://github.com/e-alizadeh/Zotero2Readwise/commit/377669a9d5326e2bd2ffea3fcb31ab09b2afd64b))

* Update link in README. ([`bdf2ffd`](https://github.com/e-alizadeh/Zotero2Readwise/commit/bdf2ffdb2b7532543901a747da9eae1d94666810))

* Use bool flag to run zotero items retrieval. ([`9b956c8`](https://github.com/e-alizadeh/Zotero2Readwise/commit/9b956c84cc677f9c7df3f22ce1e43fdfe6c96c19))

* Update default values for optional flags. ([`8d3217a`](https://github.com/e-alizadeh/Zotero2Readwise/commit/8d3217a1ad5ad60b6d247ca5f2d145da3f8f618d))

* Rename zt2rw -&gt; zotero2readwise ([`8f086d7`](https://github.com/e-alizadeh/Zotero2Readwise/commit/8f086d74b7b55659112d4985f99bcc37195b6920))

* Add a script to run the whole process. ([`9dea53d`](https://github.com/e-alizadeh/Zotero2Readwise/commit/9dea53d92de87cd1489146c740c83b0ddc9a0c14))

* Remove unused Path. ([`477b8aa`](https://github.com/e-alizadeh/Zotero2Readwise/commit/477b8aa3d16532b4b584624dc6f8d00cbe045414))

* Create a directory for failed items JSON files. ([`4ee8268`](https://github.com/e-alizadeh/Zotero2Readwise/commit/4ee82681cdb9459a444b19f57556d35f0530967f))

* Add CHANGELOG. ([`6feef46`](https://github.com/e-alizadeh/Zotero2Readwise/commit/6feef4636a480bd39245032c737249390541149c))

* Update GH action ([`5360e7b`](https://github.com/e-alizadeh/Zotero2Readwise/commit/5360e7b0d998b4580f455c06912593537bace19b))

* Move filepath handling to the method instead of class init ([`f6f9178`](https://github.com/e-alizadeh/Zotero2Readwise/commit/f6f9178dab2b6b9b9e586af51168c205b04f1a25))

* Set versions to 0.0.0.
Add Python Semantic Release.
Add Github Action Release. ([`b0833fb`](https://github.com/e-alizadeh/Zotero2Readwise/commit/b0833fb7c311f0c518b66b8c1a0075445c35a1ab))

* Add ipdb to dev dependencies. ([`e687072`](https://github.com/e-alizadeh/Zotero2Readwise/commit/e6870722648eb1bb4ed1cea01876c5500bd374e2))

* Move printout to outside the for-loop. ([`5c5b4c9`](https://github.com/e-alizadeh/Zotero2Readwise/commit/5c5b4c965afb9d978ee84b843dec8a74592d3ee6))

* Minor refactoring. ([`cec9bf5`](https://github.com/e-alizadeh/Zotero2Readwise/commit/cec9bf5b02ae5e168f229789933a0cf1daf3d413))

* Fix import error. ([`86cf280`](https://github.com/e-alizadeh/Zotero2Readwise/commit/86cf2804227a35d6abd7c47816c404c1a82dc1e9))

* Move creators concatenation to Zotero object. ([`3be7dee`](https://github.com/e-alizadeh/Zotero2Readwise/commit/3be7dee4268c4e18f1b1565a85188742adcf4b8b))

* Define ZoteroAnnotation dataclass. Define get_zotero_client() (a wrapper around Pyzotero&#39;s Zotero object). ([`73e5bb7`](https://github.com/e-alizadeh/Zotero2Readwise/commit/73e5bb7493fa35f855519c4a91ffb02b6003fe2e))

* Add setup.cfg ([`852072b`](https://github.com/e-alizadeh/Zotero2Readwise/commit/852072b0bb2357995632b8786f9631e0d5aec158))

* Add pre-commit-config. Create a zt2rw package. ([`56cf677`](https://github.com/e-alizadeh/Zotero2Readwise/commit/56cf6772c35b70aead1d76353cefe427cd1d1853))

* Update gitignore ([`b5e3563`](https://github.com/e-alizadeh/Zotero2Readwise/commit/b5e3563a14e5b62d725977776f07b3e94a2c9da5))

* Define env files. ([`9e370ae`](https://github.com/e-alizadeh/Zotero2Readwise/commit/9e370aee0cf27964874139e3e38384042d71cfea))

* Initial commit ([`32dc57d`](https://github.com/e-alizadeh/Zotero2Readwise/commit/32dc57dd7ac8b04e403c74a412a6e05d64c587ad))
