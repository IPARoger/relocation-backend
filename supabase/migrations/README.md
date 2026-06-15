# Supabase Migrations — Schema Sandbox Only

## Status

**SCHEMA SANDBOX — NOT CONNECTED TO THE APP**

Validation paused: Supabase CLI/Docker not installed. Do not apply remotely. Next valid step is local validation after installing Supabase CLI + Docker, or explicit human approval for remote sandbox apply.

This directory is reserved for **future Supabase SQL migrations** that mirror the product data model defined in:

`docs/data_model/supabase_schema_sandbox_plan_v1.md`

Local SQL migration files exist (`00001`–`00006`) but have **not** been validated locally or applied remotely. Do not apply migrations to production. Do not treat this folder as live infrastructure until explicitly approved.

---

## What this is

- A **documentation and scaffold** location for PostgreSQL schema design.
- A **future sync target** for local-first product records (accounts, clients, investigations, etc.).
- A place to version **schema changes** with explicit rollback discipline.

## What this is not

Do **not**:

- add `@supabase/supabase-js` or other Supabase client packages to the app,
- wire `map_CURRENT.html`, renderer code, or backend astrology paths to Supabase,
- replace `library/library.json` or browser `localStorage` scaffolds,
- integrate auth, RLS enforcement, or production env keys,
- migrate real user or client data,
- persist renderer output, GeoJSON, cache artifacts, or debug substrate.

**Local scaffolds remain explicitly temporary** until a governed migration slice says otherwise.

---

## Authority

| Document | Role |
|----------|------|
| `docs/data_model/supabase_schema_sandbox_plan_v1.md` | Table list, columns, relationships, JSON shapes |
| `docs/data_model/local_first_data_objects_v1.md` | Product entity doctrine, persistence boundaries |
| `docs/governance/anti_cursor_bullshit_governance_rules.md` | No hidden migrations, evidence required |

If this README conflicts with the sandbox plan v1 doc, **the plan doc wins**.

---

## Planned migration sequence (not yet created)

When SQL migrations are authorized, expected order:

| File | Purpose |
|------|---------|
| `00001_extensions.sql` | `pgcrypto` for UUID generation |
| `00002_core_entities.sql` | `professional_accounts`, `clients`, `places`, `birth_profiles` |
| `00003_work_objects.sql` | `saved_investigations`, `saved_charts`, `favorite_cities`, `comparison_sets`, `comparison_set_places` |
| `00004_settings_tags_notes.sql` | `user_settings`, `tags`, `entity_tags`, `notes` |
| `00005_indexes_constraints.sql` | Uniques, FK indexes, CHECK constraints |
| `00006_rls_stubs.sql` | **Commented-out** RLS policies for future auth — do not enable in sandbox |
| `seed/000_seed_dev_fixtures.sql` | Dev fixtures only; never production data |

---

## Apply discipline (future — local/dev only)

When migrations exist:

```bash
# Local Supabase CLI only — not production
supabase db reset
```

**Before apply:**

- [ ] Migrations reviewed against sandbox plan v1
- [ ] No renderer/map fields in JSON columns
- [ ] `settings_snapshot` required on `saved_investigations`
- [ ] Rollback order documented below

**After apply:**

- [ ] Seed fixtures insert cleanly
- [ ] JSON schema linter rejects forbidden keys (`geojson`, `renderer_substrate`, `aura`, etc.)
- [ ] No changes to app runtime behavior

---

## Rollback discipline

Drop order (reverse of create):

1. `entity_tags`, `notes`, `tags`, `user_settings`
2. `comparison_set_places`, `comparison_sets`, `favorite_cities`
3. `saved_investigations`, `saved_charts`
4. `clients`, `birth_profiles`, `places`, `professional_accounts`

Document any data wipe policy in the migration closeout. **No hidden migrations.**

---

## Saved investigation rules (must hold in all migrations)

- Store **semantic intent** in `conditions` JSONB — not renderer artifacts.
- Store **Layer 2 defaults** in `settings_snapshot` at save time.
- Support reopen modes: `keep_snapshot` | `use_current` (see plan doc §2).
- Reference **stable `places.id`** for favorites and comparisons.

---

## RLS and auth

**Current phase:** no Row Level Security enabled. No auth integration.

`00006_rls_stubs.sql` (when written) will contain **commented** policy templates only. Enabling RLS requires a separate approved slice with auth wiring — out of scope for schema sandbox.

---

## Relationship to existing scaffolds

| Scaffold | Status |
|----------|--------|
| `library/library.json` | Active dev scaffold; **not** superseded by Supabase |
| Phase 2.3 saved investigation replay | Source shape for `conditions`; add `settings_snapshot` on migration |
| Browser `localStorage` | Onboarding/session only; not product DB |

A future adapter may **export** mirror JSON → Supabase or **import** for dev testing. That adapter is not authorized yet.

---

## Next step (when approved)

Author `00001`–`00005` SQL from `docs/data_model/supabase_schema_sandbox_plan_v1.md`, then run local `supabase db reset` and capture validation evidence.

**Until then:** this directory contains documentation only.
