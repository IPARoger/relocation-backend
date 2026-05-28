# Supabase Schema Sandbox Plan v1

## Status

**PLANNING ONLY — SCHEMA SANDBOX**

This document defines a **local-first schema plan** that can later mirror to Supabase. It is **not** implementation, **not** a runtime dependency, and **not** authorized to replace existing scaffolds.

**Reads with:** `docs/data_model/local_first_data_objects_v1.md`, `docs/future/birth_time_uncertainty_and_confidence_doctrine.md`, `validation/narratives/phase2_3_saved_investigation_replay.md`, `library/library.json` (legacy scaffold).

---

## Explicit non-goals (current phase)

Do **not**:

- integrate auth or Supabase client packages,
- wire app flows to Supabase,
- replace `localStorage` or `library/library.json`,
- create production dependency,
- migrate real data,
- touch renderer or map code,
- persist renderer artifacts, GeoJSON, cache output, or debug substrate.

Supabase is a **schema mirror / future sync target** only.

---

## Architectural boundary

```text
┌─────────────────────────────────────────────────────────┐
│  PRODUCT RECORDS (local-first → future Supabase sync)   │
│  accounts, clients, birth_profiles, investigations, etc.  │
└───────────────────────────┬─────────────────────────────┘
                            │ references
┌───────────────────────────▼─────────────────────────────┐
│  SEMANTIC CACHE (ephemeral — NOT in Supabase product)   │
└───────────────────────────┬─────────────────────────────┘
                            │ hydrates (dev only)
┌───────────────────────────▼─────────────────────────────┐
│  RENDERER / DISPLAY (never persisted as truth)          │
└─────────────────────────────────────────────────────────┘
```

---

## 1. Proposed table list

| # | Table | Role |
|---|--------|------|
| 1 | `professional_accounts` | Professional owner (future auth subject; no auth now) |
| 2 | `clients` | One client per professional; one birth profile (MVP) |
| 3 | `birth_profiles` | Natal Layer 1 input domain |
| 4 | `places` | Stable place identity (geoname/WOF/manual/map pick) |
| 5 | `saved_charts` | Relocated chart = birth profile + place |
| 6 | `saved_investigations` | Saved search / investigation (`saved_searches` in product language) |
| 7 | `favorite_cities` | Client-scoped place bookmark |
| 8 | `comparison_sets` | Ordered place shortlist for one client |
| 9 | `comparison_set_places` | Join: comparison set ↔ place (ordered) |
| 10 | `user_settings` | Account-level Layer 2 defaults (1:1 with account) |
| 11 | `tags` | Account-scoped tag definitions |
| 12 | `entity_tags` | Polymorphic tag assignments |
| 13 | `notes` | Polymorphic professional notes |

**Naming:** SQL table is `saved_investigations`. Product/UI may say “saved search.”

---

## 2. Columns per table

### `professional_accounts`

| Column | Type | Notes |
|--------|------|-------|
| `id` | `uuid` PK | `gen_random_uuid()` |
| `display_name` | `text` NOT NULL | |
| `email` | `text` UNIQUE NULL | reserved for future auth; nullable in sandbox |
| `schema_version` | `smallint` NOT NULL DEFAULT 1 | |
| `created_at` | `timestamptz` NOT NULL DEFAULT now() | |
| `updated_at` | `timestamptz` NOT NULL DEFAULT now() | |
| `deleted_at` | `timestamptz` NULL | soft delete |

---

### `clients`

| Column | Type | Notes |
|--------|------|-------|
| `id` | `uuid` PK | |
| `account_id` | `uuid` NOT NULL FK → `professional_accounts.id` | |
| `display_name` | `text` NOT NULL | professional's label |
| `birth_profile_id` | `uuid` NOT NULL FK → `birth_profiles.id` UNIQUE | one natal chart per client (MVP) |
| `schema_version` | `smallint` NOT NULL DEFAULT 1 | |
| `created_at` | `timestamptz` | |
| `updated_at` | `timestamptz` | |
| `deleted_at` | `timestamptz` NULL | |

---

### `birth_profiles`

| Column | Type | Notes |
|--------|------|-------|
| `id` | `uuid` PK | |
| `birth_date` | `date` NOT NULL | |
| `birth_time` | `time` NULL | null when T3 unknown |
| `birth_place_id` | `uuid` NOT NULL FK → `places.id` | |
| `timezone_id` | `text` NOT NULL | IANA |
| `utc_offset_at_birth_minutes` | `integer` NULL | audit / DST edge cases |
| `confidence_tier` | `text` NOT NULL | `T0`–`T4`; see birth-time doctrine |
| `confidence_metadata` | `jsonb` NOT NULL DEFAULT `{}` | range, source, solar policy |
| `representative_time` | `time` NULL | explicit only; never implicit guess |
| `layer1_snapshot_hash` | `text` NULL | optional recompute detection |
| `schema_version` | `smallint` NOT NULL DEFAULT 1 | |
| `created_at` | `timestamptz` | |
| `updated_at` | `timestamptz` | |

**Must not store:** rendered houses, popup strings, GeoJSON.

---

### `places`

| Column | Type | Notes |
|--------|------|-------|
| `id` | `uuid` PK | internal stable ID |
| `external_source` | `text` NOT NULL | `geoname`, `wof`, `manual`, `map_pick` |
| `external_id` | `text` NULL | geoname ID etc. |
| `display_name` | `text` NOT NULL | |
| `admin1` | `text` NULL | state/region |
| `country_code` | `char(2)` NULL | ISO |
| `country_name` | `text` NULL | readable disambiguation |
| `lat` | `double precision` NOT NULL | |
| `lon` | `double precision` NOT NULL | |
| `resolution_audit` | `jsonb` NOT NULL DEFAULT `{}` | geocoder candidate chosen |
| `schema_version` | `smallint` NOT NULL DEFAULT 1 | |
| `created_at` | `timestamptz` | |

**Unique:** `(external_source, external_id)` WHERE `external_id IS NOT NULL`.

Favorites and comparisons reference `places.id`, not raw search strings.

---

### `saved_charts`

Relocated chart = natal + destination place (distinct from saved investigation).

| Column | Type | Notes |
|--------|------|-------|
| `id` | `uuid` PK | |
| `client_id` | `uuid` NOT NULL FK → `clients.id` | |
| `birth_profile_id` | `uuid` NOT NULL FK → `birth_profiles.id` | must match client's profile |
| `place_id` | `uuid` NOT NULL FK → `places.id` | relocation location |
| `title` | `text` NULL | |
| `point_truth_cache` | `jsonb` NULL | optional API memo; not map tiles |
| `computed_at` | `timestamptz` NULL | last point-truth fetch |
| `schema_version` | `smallint` NOT NULL DEFAULT 1 | |
| `created_at` | `timestamptz` | |
| `updated_at` | `timestamptz` | |

**Unique (MVP):** `(client_id, place_id)`.

---

### `saved_investigations`

Product synonym: **saved searches**.

| Column | Type | Notes |
|--------|------|-------|
| `id` | `uuid` PK | |
| `client_id` | `uuid` NOT NULL FK → `clients.id` | |
| `birth_profile_id` | `uuid` NOT NULL FK → `birth_profiles.id` | snapshot anchor |
| `title` | `text` NOT NULL | |
| `conditions` | `jsonb` NOT NULL | semantic intent only |
| `viewport` | `jsonb` NOT NULL | center, zoom, bounds |
| `settings_snapshot` | `jsonb` NOT NULL | Layer 2 at save time |
| `settings_snapshot_version` | `smallint` NOT NULL DEFAULT 1 | |
| `layer_display_state` | `jsonb` NOT NULL DEFAULT `{}` | mute/solo/z-order (display only) |
| `default_reopen_mode` | `text` NOT NULL DEFAULT `keep_snapshot` | `keep_snapshot` \| `use_current` |
| `source_investigation_id` | `uuid` NULL FK → `saved_investigations.id` | fork/duplicate lineage |
| `schema_version` | `smallint` NOT NULL DEFAULT 1 | |
| `created_at` | `timestamptz` | |
| `updated_at` | `timestamptz` | |

**Explicitly absent:** `geojson`, `renderer_substrate`, `canvas`, `aura_*`, `cache_*`, `debug_*`.

#### `conditions` JSON (v1)

Backward-compatible with Phase 2.3 `library/library.json` shape; target flexible `overlay_conditions[]`:

```json
{
  "schema_version": 1,
  "kind": "saved_investigation",
  "overlay_conditions": [
    {
      "id": "cond_uuid",
      "type": "planet_in_house",
      "polarity": "include",
      "parameters": { "planet": "moon", "house": 4 },
      "display_color_key": "house_a"
    }
  ]
}
```

Legacy fields (`house_conditions`, `angle_sign_conditions`, `aspect_overlay`) may appear during transition.

#### `settings_snapshot` JSON (Layer 2 only)

```json
{
  "house_system": "placidus",
  "zodiac_mode": "tropical",
  "orb_defaults": { "conjunction": 8, "square": 6 },
  "visible_minor_aspects": false,
  "helper_layers": {},
  "ontology_pack_id": null
}
```

#### Reopen behavior

| Mode | Behavior |
|------|----------|
| `keep_snapshot` | Replay uses `settings_snapshot`; badge if current settings differ |
| `use_current` | Replay uses live `user_settings`; conditions unchanged; confirm if diff |

Per-investigation `default_reopen_mode` stores user preference; UI may prompt on each reopen.

---

### `favorite_cities`

| Column | Type | Notes |
|--------|------|-------|
| `id` | `uuid` PK | |
| `client_id` | `uuid` NOT NULL FK → `clients.id` | |
| `place_id` | `uuid` NOT NULL FK → `places.id` | |
| `saved_investigation_id` | `uuid` NULL FK | optional lineage |
| `sort_order` | `integer` NULL | |
| `schema_version` | `smallint` NOT NULL DEFAULT 1 | |
| `created_at` | `timestamptz` | |

**Unique:** `(client_id, place_id)`.

---

### `comparison_sets`

| Column | Type | Notes |
|--------|------|-------|
| `id` | `uuid` PK | |
| `client_id` | `uuid` NOT NULL FK → `clients.id` | |
| `title` | `text` NOT NULL | |
| `saved_investigation_id` | `uuid` NULL FK | optional parent context |
| `birth_profile_id` | `uuid` NOT NULL FK | chart used for comparison |
| `schema_version` | `smallint` NOT NULL DEFAULT 1 | |
| `created_at` | `timestamptz` | |
| `updated_at` | `timestamptz` | |

---

### `comparison_set_places`

| Column | Type | Notes |
|--------|------|-------|
| `comparison_set_id` | `uuid` FK → `comparison_sets.id` ON DELETE CASCADE | |
| `place_id` | `uuid` FK → `places.id` | |
| `sort_order` | `smallint` NOT NULL | |
| `annotation` | `text` NULL | per-city note |
| PRIMARY KEY | `(comparison_set_id, place_id)` | |

---

### `user_settings`

| Column | Type | Notes |
|--------|------|-------|
| `account_id` | `uuid` PK FK → `professional_accounts.id` | 1:1 |
| `settings` | `jsonb` NOT NULL | Layer 2 defaults |
| `settings_version` | `smallint` NOT NULL DEFAULT 1 | |
| `updated_at` | `timestamptz` | |

Changing account defaults does **not** retroactively rewrite saved investigations without user action.

---

### `tags`

| Column | Type | Notes |
|--------|------|-------|
| `id` | `uuid` PK | |
| `account_id` | `uuid` NOT NULL FK → `professional_accounts.id` | |
| `name` | `text` NOT NULL | |
| `color_key` | `text` NULL | UI only |
| `created_at` | `timestamptz` | |

**Unique:** `(account_id, lower(name))`.

---

### `entity_tags`

| Column | Type | Notes |
|--------|------|-------|
| `tag_id` | `uuid` FK → `tags.id` | |
| `entity_type` | `text` NOT NULL | `client`, `saved_investigation`, `saved_chart`, `comparison_set` |
| `entity_id` | `uuid` NOT NULL | |
| PRIMARY KEY | `(tag_id, entity_type, entity_id)` | |

---

### `notes`

| Column | Type | Notes |
|--------|------|-------|
| `id` | `uuid` PK | |
| `account_id` | `uuid` NOT NULL FK | author scope |
| `entity_type` | `text` NOT NULL | above + `birth_profile` |
| `entity_id` | `uuid` NOT NULL | |
| `body` | `text` NOT NULL | |
| `created_at` | `timestamptz` | |
| `updated_at` | `timestamptz` | |

---

## 3. Relationships

```text
professional_accounts 1──1 user_settings
professional_accounts 1──N clients
professional_accounts 1──N tags

clients 1──1 birth_profiles (MVP)
clients 1──N saved_investigations
clients 1──N favorite_cities
clients 1──N comparison_sets
clients 1──N saved_charts

birth_profiles N──1 places (birth_place)
saved_charts N──1 places (relocation place)
favorite_cities N──1 places
comparison_set_places N──1 places

saved_investigations N──1 birth_profiles
comparison_sets N──1 saved_investigations (optional)

tags N──M entities via entity_tags
notes ── polymorphic ── entities + birth_profile
```

---

## 4. JSON vs normalized fields

| JSONB | Normalized |
|-------|------------|
| `saved_investigations.conditions` | accounts, clients, FK graph |
| `saved_investigations.settings_snapshot` | `places` core columns |
| `saved_investigations.viewport` | `confidence_tier` on birth_profiles |
| `saved_investigations.layer_display_state` | `comparison_set_places.sort_order` |
| `user_settings.settings` | tag/note polymorphic keys |
| `birth_profiles.confidence_metadata` | |
| `places.resolution_audit` | |
| `saved_charts.point_truth_cache` | |

**Future lint rule:** reject renderer keys in persisted JSON (`geojson`, `renderer_substrate`, `aura`, `cache`, `debug`).

---

## 5. Migration file plan (not yet authored)

Planned files under `supabase/migrations/` when approved:

| File | Contents |
|------|----------|
| `00001_extensions.sql` | `pgcrypto` |
| `00002_core_entities.sql` | accounts, clients, places, birth_profiles |
| `00003_work_objects.sql` | investigations, saved_charts, favorites, comparisons |
| `00004_settings_tags_notes.sql` | user_settings, tags, entity_tags, notes |
| `00005_indexes_constraints.sql` | uniques, FK indexes, CHECK constraints |
| `00006_rls_stubs.sql` | commented RLS for future auth — do not enable in sandbox |
| `seed/000_seed_dev_fixtures.sql` | fake dev rows only |

See `supabase/migrations/README.md` for sandbox rules and apply/rollback discipline.

---

## 6. Local JSON mirror schema

Temporary scaffold only. Proposed path: `scaffold/local_mirror/TEMPORARY_product_store.json` (not created until approved).

```json
{
  "_storage": "TEMPORARY_LOCAL_SCAFFOLD",
  "_warning": "NOT PRODUCT STORAGE. NOT AUTHORITATIVE. DO NOT SYNC WITHOUT EXPLICIT MIGRATION.",
  "storage_schema_version": 1,
  "supabase_mirror_version": 1,
  "professional_accounts": [],
  "clients": [],
  "birth_profiles": [],
  "places": [],
  "saved_charts": [],
  "saved_investigations": [],
  "favorite_cities": [],
  "comparison_sets": [],
  "comparison_set_places": [],
  "user_settings": [],
  "tags": [],
  "entity_tags": [],
  "notes": []
}
```

### Legacy mapping (`library/library.json`)

| Legacy | Mirror table |
|--------|----------------|
| `charts[]` | `birth_profiles` + stub `clients` + `places` |
| `views[]` | `saved_investigations` |
| `views[].conditions[]` | `saved_investigations.conditions` |
| `views[].viewport` | `saved_investigations.viewport` |
| `favorites[]` | `favorite_cities` + `places` |
| `settings` | `user_settings.settings` |

**Gap vs Phase 2.3:** add `settings_snapshot` on save (required for reopen doctrine).

Existing `library/library.json` remains **unchanged** until an explicit migration slice is approved.

---

## 7. Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Supabase becomes silent product DB | High | README banner; no app imports |
| `library.json` promoted without migration | High | separate paths; adapter later |
| Investigations without `settings_snapshot` | High | NOT NULL in SQL when migrations land |
| `use_current` reopen silently shifts truth | High | diff UI + confirmation |
| Places without external ID | Medium | `manual`/`map_pick`; internal UUID stable |
| `point_truth_cache` mistaken for truth | Medium | popup/API remains authority |
| JSON conditions shape drift | Medium | `schema_version` + validator |
| RLS enabled too early | Medium | stubs commented only |
| Auth columns tempt integration | Low | nullable email; no client SDK |

---

## 8. Layer 1 vs Layer 2 in storage

| Data | Layer |
|------|-------|
| Birth datetime, place, ephemeris inputs | L1 |
| House system, zodiac mode | L1 compute parameter |
| Orb defaults, minor aspects, helper layers | L2 → `user_settings` + `settings_snapshot` |
| Ontology packs | L2 |
| Conditions in investigations | L1 semantic requests |

Layer 2 must not alter Layer 1 membership. Snapshots preserve honest replay.

---

## 9. First implementation step (when approved)

1. Author SQL migrations `00001`–`00005` per §5.
2. Add JSON schemas: `schemas/saved_investigation_conditions.v1.json`, `schemas/settings_snapshot.v1.json`.
3. Run `supabase db reset` on **local/dev project only**.
4. Validate: seed insert; linter rejects renderer keys in `conditions`.

**Do not:** add Supabase client packages, env keys to app, or change `map_CURRENT.html` / renderer paths.

---

## Revision

Revise when: flexible condition rows ship, auth integration is approved, or legacy `library.json` migration is scheduled. Bump `supabase_mirror_version` on breaking JSON shape changes.
