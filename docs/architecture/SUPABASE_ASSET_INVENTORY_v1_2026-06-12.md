# Supabase Asset Inventory

**Status:** Verified live snapshot (for AI/engineer handoff)
**Date:** 2026-06-12
**Project ref:** `dpmtmmryvlftfahipowa` (`https://dpmtmmryvlftfahipowa.supabase.co`)

## How this was verified

- **Live introspection** via PostgREST OpenAPI (`/rest/v1/`), table probes (service-role + anon keys), GoTrue settings (`/auth/v1/settings`), Storage `list_buckets`, and Functions reachability — all run 2026-06-12.
- **On-disk** migration SQL + `.env` read for definitions.
- **Caveat:** `pg_catalog` is not reachable through the API keys available, so **indexes and RLS enablement are reported from applied migration DDL + observed runtime behavior**, not from a direct catalog read. Items needing dashboard/`psql` confirmation are flagged ⚠️.

Legend: ✅ implemented/live · 🟡 partial/needs reconciliation · 🔲 proposed (on disk only, not applied)

---

## 1. Tables — ✅ 15 live (public schema)

All have `id uuid PK default gen_random_uuid()` and timestamptz `created_at`. Row counts are live (service-role).

| Table | Rows | Key columns | FKs | Notes |
|-------|-----:|-------------|-----|-------|
| `profiles` | 3 | `account_user_id` (uuid, not null), `display_name`, `profile_type` | — (root) | Top of tree. `account_user_id` = intended `auth.users.id` |
| `places` | 21 | `provider`, `provider_place_id`, `geonames_id`, `display_name`, `canonical_name`, `admin1/2`, `country_code/name`, `latitude/longitude`, `timezone_id`, `population`, `importance_rank`, `language_code`, `alternate_names_json` | — | Multilingual-ready (`language_code` + `alternate_names_json`) |
| `birth_records` | 3 | `birth_date`, `birth_time_mode`, `birth_time_start/end`, `timezone_id`, `utc_datetime_start/end`, `chart_settings_json`, `archived_at` | `profile_id`→profiles, `birth_place_id`→places | Birth-time uncertainty range supported |
| `intention_profiles` | 0 | `title`, `intention_type`, `settings_json` | `profile_id`→profiles | |
| `current_location_history` | 0 | `selected_at`, `is_current`, `source` | `profile_id`→profiles, `place_id`→places | |
| `location_events` | 0 | `event_type`, `event_source`, `occurred_at`, `lat/long`, `metadata_json` | `profile_id`→profiles, `place_id`→places | |
| `favorite_places` | 18 | `label`, `rank`, `starred`, `archived_at` | `profile_id`→profiles, `place_id`→places | `unique(profile_id, place_id)` |
| `visited_places` | 1 | `visited_at`, `source`, `notes` | `profile_id`→profiles, `place_id`→places | `unique(profile_id, place_id)` |
| `saved_searches` | 2 | `title`, `search_type`, `conditions_json`, `viewport_json`, `settings_snapshot_json`, `date_start/end` | `profile_id`→profiles | Genie searches |
| `comparison_sets` | 2 | `title`, `settings_snapshot_json` | `profile_id`→profiles | |
| `comparison_set_places` | 0 | `sort_order`, `role` | `comparison_set_id`→comparison_sets, `place_id`→places | `unique(comparison_set_id, place_id)` |
| `notes` | 2 | `target_type`, `target_id`, `section_key`, `title`, `body` | `profile_id`→profiles | Polymorphic target |
| `user_settings` | 2 | `account_user_id`, `settings_json` | `profile_id`→profiles (nullable) | **Account-level (profile_id null) AND per-profile** both supported |
| `share_links` | 2 | `slug` (unique), `target_type/id`, `visibility`, `hide_birth_data`, `include_*`, `expires_at`, `revoked_at` | `profile_id`→profiles | |
| `profile_relationships` | 0 | `account_user_id`, `relationship_type`, `label` | `profile_a_id`/`profile_b_id`→profiles | |

`intention_profile_id` (uuid, nullable, not enforced as FK in OpenAPI) appears on `favorite_places`, `saved_searches`, `comparison_sets`, `notes`.

---

## 2. Extensions — ✅

- `pgcrypto` (for `gen_random_uuid()`) — created in applied schema.

---

## 3. Indexes — ✅ 20 defined in applied migration ⚠️ (catalog not re-read)

From `2026_06_08_schema_v1.sql` (lines 208–227):

`idx_profiles_account_user_id`, `idx_birth_records_profile_id`, `idx_places_country_name`, `idx_places_display_name`, `idx_places_timezone_id`, `idx_current_location_profile_id`, `idx_location_events_profile_id`, `idx_favorite_places_profile_id`, `idx_visited_places_profile_id`, `idx_saved_searches_profile_id`, `idx_comparison_sets_profile_id`, `idx_notes_profile_id`, `idx_notes_target (target_type,target_id)`, `idx_share_links_slug`, `idx_intention_profiles_profile_id`, `idx_favorite_places_intention_profile_id`, `idx_saved_searches_intention_profile_id`, `idx_comparison_sets_intention_profile_id`, `idx_notes_intention_profile_id`.

Plus implicit PK indexes (15) and unique-constraint indexes (`favorite_places`, `visited_places`, `comparison_set_places`, `share_links.slug`).

---

## 4. RLS policies — 🟡 enabled, default-deny, **0 policies**

**Observed runtime behavior:** with the anon (publishable) key, `SELECT` on every table returns **0 rows with no error**, while the service-role key returns full counts. That signature means **RLS is ENABLED on all 15 tables but NO policies are defined** (default-deny). Anon has table privileges (no permission error), so rows are filtered by RLS, not by GRANT.

**Discrepancy to reconcile:** the applied migration (`2026_06_08_schema_v1.sql`) contains **no `ENABLE ROW LEVEL SECURITY` and no `CREATE POLICY`** statements. So RLS was enabled **out-of-band** (Supabase dashboard or ad-hoc SQL), not via tracked migrations. ⚠️ Confirm in dashboard and codify into a migration.

**Proposed (not applied):** `00006_rls_stubs.sql` contains fully **commented-out** policy templates — and they reference **dead/old table names** (`professional_accounts`, `clients`, `favorite_cities`, `tags`), so they are stale and cannot be uncommented as-is.

**Net:** real users cannot read their own data yet (no policy grants access); everything currently runs through the service-role key. Policies keyed to `auth.uid() = profiles.account_user_id` (and child tables via `profile_id → profiles`) still need to be written.

---

## 5. Auth — 🟡 email only

From `/auth/v1/settings` (live):

- **Enabled provider:** `email` ✅
- **Disabled (all OAuth/social):** apple, google, facebook, azure, github, gitlab, bitbucket, discord, figma, kakao, keycloak, linkedin, linkedin_oidc, notion, slack, slack_oidc, snapchat, spotify, twitch, twitter, workos, zoom, fly, phone, anonymous_users — **all `false`**.
- `disable_signup`: **false** (signups allowed)
- `mailer_autoconfirm`: **false** (email confirmation required)
- **Auth users currently in project: 0** (verified via admin `list_users`). Existing data rows therefore use a placeholder `account_user_id = 00000000-0000-0000-0000-000000000000`.

Decided (founder) but **not yet enabled**: Google + Apple OAuth (Email already on).

---

## 6. Storage buckets — ✅ none

`list_buckets()` → empty. No buckets, no objects, no storage policies.

---

## 7. Edge Functions — ✅ none

- No `supabase/functions/` directory on disk.
- `/functions/v1/` base returns 404 (no deployed functions enumerable via available keys). ⚠️ Full enumeration would need the Management API / personal access token.

---

## 8. Migrations on disk

| File | State |
|------|-------|
| `2026_06_08_schema_v1.sql` | ✅ **Applied** — matches live schema + `repositories/` |
| `2026_06_08_birth_records_archived_at.sql` | ✅ Applied (adds `birth_records.archived_at`) |
| `00001_extensions.sql` | 🔲 Superseded (old sandbox set) |
| `00002_core_entities.sql` | 🔲 Superseded — uses dead names (`professional_accounts`, `clients`, `birth_profiles`) |
| `00003_work_objects.sql` | 🔲 Superseded (`saved_investigations`, `saved_charts`, `favorite_cities`) |
| `00004_settings_tags_notes.sql` | 🔲 Superseded (`tags`, `entity_tags`) |
| `00005_indexes_constraints.sql` | 🔲 Superseded |
| `00006_rls_stubs.sql` | 🔲 Proposed, commented out, **stale table names** |
| `README.md` | ⚠️ **Out of date** — says "sandbox, not applied"; live DB contradicts it |

No `supabase/config.toml` (CLI not linked locally). No `seed/` directory.

---

## 9. Environment variables (`.env`)

| Key | State | Value / note |
|-----|-------|--------------|
| `SUPABASE_URL` | ✅ set | `https://dpmtmmryvlftfahipowa.supabase.co` |
| `SUPABASE_ANON_KEY` | ✅ set | **new-format** `sb_publishable_…` (browser-safe, RLS-gated) |
| `SUPABASE_SERVICE_ROLE_KEY` | ✅ set | **new-format** `sb_secret_…` (server-only; bypasses RLS) |
| `GEOAPIFY_API_KEY` | 🔲 EMPTY | Layer-B autocomplete not yet provisioned |
| `CITY_PROVIDER` | ✅ set | `geoapify` |
| `DEFAULT_LANGUAGE` | ✅ set | `en` |
| `DEFAULT_COUNTRY_DISPLAY` | ✅ set | `en` |
| `TIMEZONE_PROVIDER` | ✅ set | `iana` |
| `TIMEZONE_LOOKUP_MODE` | in `.env.example` only | `offline_timezonefinder_plus_zoneinfo` |

Not present (needed later): `MAPTILER_API_KEY` (Layer C), `DEEPL_API_KEY` (Layer E), Google/Apple OAuth client IDs/secrets (set in Supabase dashboard, not `.env`).

> Key-format note: both keys are the **2025 new Supabase key format** (`sb_publishable_…` / `sb_secret_…`), not legacy JWT `anon`/`service_role` tokens. Client libs handle both, but RLS still applies to the publishable key.

---

## 10. Implemented vs proposed — one-glance

| Asset | Implemented (live) | Proposed / missing |
|-------|--------------------|--------------------|
| Tables | ✅ 15 (with data) | — |
| Extensions | ✅ pgcrypto | — |
| Indexes | ✅ 20 + PK/unique | — |
| RLS enabled | 🟡 yes (default-deny) | codify in migration |
| RLS policies | ❌ none | 🔲 write `auth.uid()=account_user_id` tree policies |
| Auth: email | ✅ on | — |
| Auth: Google/Apple OAuth | ❌ | 🔲 enable (decided) |
| Auth users | ❌ 0 | 🔲 first real signup |
| Storage buckets | ❌ none | 🔲 if avatars/exports needed |
| Edge functions | ❌ none | 🔲 chart/timezone math, DeepL proxy (TBD) |
| Frontend ↔ Supabase | ❌ localStorage only | 🔲 wire settings/notes/etc. |
| City autocomplete (Geoapify) | ❌ key empty | 🔲 provision + wire |
| Map tiles (MapTiler) | ❌ | 🔲 single-language labels |
| Translation (DeepL) | ❌ | 🔲 AI/UI/overlay/notes |

---

## 11. Immediate reconciliation items for the next builder

1. **Codify RLS**: confirm dashboard RLS state, then add a tracked migration that (a) `ENABLE ROW LEVEL SECURITY` per table and (b) defines policies on `profiles.account_user_id = auth.uid()` with child tables joined via `profile_id`.
2. **Delete/quarantine** dead migrations `00001–00006` (or move to `migrations/_archive/`) so they don't get applied.
3. **Fix `migrations/README.md`** — it falsely says "sandbox, not applied."
4. **Wire Supabase Auth** (Email live; enable Google + Apple) and replace placeholder `account_user_id` once a real user exists; decide whether to migrate existing 00000-account test rows.
5. **`places` privacy**: decide whether `places` (shared reference data) should be world-readable (public SELECT policy) vs per-account — currently default-denied to anon like everything else.
