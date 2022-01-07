# CHANGELOG

<!--next-version-placeholder-->

## v0.2.3 (2022-01-07)
### Fix
* Use alternate link Zotero (`https://www.zotero.org/username/items/<itemKey>`) that has a html content instead of self link (`https://api.zotero.org/users/<userID>/items/<itemKey>`) that contains a JSON content and calls the API. ([`3310ad1`](https://github.com/e-alizadeh/Zotero2Readwise/commit/3310ad130afdcc977a8eb771712950d0d70064d1))

## v0.2.2 (2022-01-03)
### Fix
* An oversight in `Zotero2Readwise` class method `run()` (previously `run_all())` ([`e2b1336`](https://github.com/e-alizadeh/Zotero2Readwise/commit/e2b133634372b44cefc728923ae7ef384c69adda))

## v0.2.1 (2022-01-03)
### Fix
* Get non-empty objects from ZoteroItem (so that we have a JSON serializable object) ([`6b79fc9`](https://github.com/e-alizadeh/Zotero2Readwise/commit/6b79fc9bf457acd78287a8f0cbe1800f335e52fc))
* Ignore highlights more than 8191 characters (readwise limit for a highlight.) ([`7503324`](https://github.com/e-alizadeh/Zotero2Readwise/commit/7503324150d50db72abd3c3cbfda8b469a7d596d))

### Documentation
* Improve printouts for both Zotero and Readwise operations ([`5a22717`](https://github.com/e-alizadeh/Zotero2Readwise/commit/5a22717987a509c123b233dfd33aeded1a9902cd))
* Define Zotero2ReadwiseError exception object. ([`7d5022a`](https://github.com/e-alizadeh/Zotero2Readwise/commit/7d5022a0ebc28e170e07dc004042981b2be7e314))

## v0.2.0 (2022-01-01)
### Feature
* Refactor `Zotero2Readwise.run()` to pass a custom number of Zotero annotations and notes instead of running all. ([`7c8a337`](https://github.com/e-alizadeh/Zotero2Readwise/commit/7c8a3372b642e3056c5279dcfa06470eb6981f34))

### Fix
* Remove filtering zotero items upto 5 items. ([`4f3e5e0`](https://github.com/e-alizadeh/Zotero2Readwise/commit/4f3e5e097ec9f6b99e709c1b3be306802a672023))

## v0.1.1 (2022-01-01)
### Fix
* Project details ([`502806c`](https://github.com/e-alizadeh/Zotero2Readwise/commit/502806cceb8f03a8bc2ae2d3f6d79a202d7e9452))

## v0.1.0 (2022-01-01)
First release