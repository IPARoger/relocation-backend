# Local Product Store v2

## Status

**TEMPORARY_LOCAL_SCAFFOLD — Phase 3.0a file-only slice**

Parallel to `library/library.json`. Not connected to map, HTTP, Supabase, or UI.

**Reads with:** `docs/data_model/local_first_data_objects_v1.md`, `docs/data_model/supabase_schema_sandbox_plan_v1.md`.

---

## Purpose

Provide a local-first JSON persistence shape for:

- professional account scaffold (single embedded account),
- clients,
- one birth profile per client,
- saved investigations / searches with `settings_snapshot`,
- favorite cities with stable `place_id` references,
- optional inline client `notes` and `tags[]`.

---

## File location

```text
scaffold/local_product/TEMPORARY_product_store.json   # committed empty template
```

Runtime smokes write to **temp paths** only. Do not promote this file to product storage without explicit migration approval.

---

## Python module

`local_product_store.py`:

| Function | Role |
|----------|------|
| `empty_store()` | Fresh v2 document with TEMPORARY markers |
| `load(path)` | Read JSON |
| `save(state, path)` | Validate then atomic write (`mkstemp` + `os.replace`) |
| `validate_store(state)` | Structural + forbidden-key checks |
| `create_client(...)` | Client + birth_profile + birth place |
| `save_investigation(...)` | Requires `settings_snapshot` (defaults from `user_settings`) |
| `add_favorite_city(...)` | Client-scoped place bookmark |

---

## Validation rules

- `_storage` must be `TEMPORARY_LOCAL_SCAFFOLD`
- `storage_schema_version` must be `2`
- Each client references exactly one unique `birth_profile_id`
- Each `saved_investigation` must include `settings_snapshot` (object)
- Forbidden key substrings in investigation JSON and user_settings:  
  `geojson`, `renderer_substrate`, `canvas`, `aura`, `virga`, `cache`, `debug`

---

## Scripts

```bash
./venv/bin/python scripts/validate_local_product_store.py
./venv/bin/python scripts/smoke_local_product_store.py
```

---

## Explicit non-goals (Phase 3.0a)

- No HTTP routes
- No `library.json` migration
- No map / renderer integration
- No Supabase apply
- No UI
- No `saved_charts`, comparison sets, or polymorphic notes table

---

## Rollback

Delete:

- `local_product_store.py`
- `scaffold/local_product/`
- `schemas/local_product_store.v2.json`
- `scripts/validate_local_product_store.py`
- `scripts/smoke_local_product_store.py`
- this document

No other files are affected.

---

## Revision

Bump `storage_schema_version` on breaking shape changes. Keep aligned with `supabase_schema_sandbox_plan_v1.md` when Supabase migrations are applied locally.
