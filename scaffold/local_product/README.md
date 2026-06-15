# Local Product Store — TEMPORARY SCAFFOLD

## Status

**TEMPORARY_LOCAL_SCAFFOLD — NOT PRODUCT STORAGE**

This directory holds the Phase 3.0a local-first product store file mirror. It is **parallel** to `library/library.json` and does **not** replace it.

## Rules

- Do not treat this file as authoritative product storage.
- Do not wire `map_CURRENT.html` or `/library/*` to this path without explicit approval.
- Do not migrate `library/library.json` automatically.
- Supabase remains schema sandbox only; no remote sync from here.

## Files

| File | Purpose |
|------|---------|
| `TEMPORARY_product_store.json` | Empty v2 template (committed) |
| User/runtime copies | Smokes write to temp paths; production use not authorized |

## Module

Python API: `local_product_store.py` at repo root.

Validation: `scripts/validate_local_product_store.py`

Smoke: `scripts/smoke_local_product_store.py`

## Doctrine

See `docs/data_model/local_product_store_v2.md` and `docs/data_model/local_first_data_objects_v1.md`.
