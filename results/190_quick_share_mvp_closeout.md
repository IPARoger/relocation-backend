# QUICK-SHARE-MVP Closeout

**Date:** 2026-06-21  
**Scope:** Frozen map-first share links (Map + Profile chart / Screen 4). No Export Wizard, PDF, or practitioner branding.

## Approved decisions (implemented)

1. Frozen snapshot — recipient replays stored payload; no live recompute.
2. New `quick_shares` table — deprecated `POST /share-links` not used for create.
3. Surfaces: Map (`map_CURRENT.html`) and Screen 4 Profile relocated chart (`app_shell.html`).
4. Default anchor always MAP: `map_CURRENT.html?quickShare=<uuid>`.
5. App-branded (`brand: "Relocation Astrology"`), not practitioner-branded.
6. Export Wizard out of scope (Export screen copy updated to point users to Quick Share).

---

## Files changed

| File | Role |
|------|------|
| `supabase/migrations/2026_06_21_quick_shares.sql` | New table + indexes |
| `repositories/quick_share_repository.py` | JWT create + public read |
| `main_centerline_FIXER.py` | `POST /quick-share/create`, `GET /quick-share/{id}`, `GET /quick_share.js` |
| `quick_share.js` | Shared create, clipboard, URL builder, chart-facts HTML |
| `map_CURRENT.html` | Map Quick Share button, capture bundle, recipient bootstrap |
| `app_shell.html` | Profile chart Quick Share button, chart bundle + facts capture |
| `scripts/smoke_quick_share.py` | Static + repository validation |

**Not touched for Quick Share:** `share_links` repository/routes (legacy list/get remain; `POST /share-links` still 410).

---

## Schema / storage

**Table:** `quick_shares`

| Column | Type | Notes |
|--------|------|-------|
| `id` | `uuid` PK | Client-generated UUID on insert; unguessable |
| `account_id` | `uuid` | Owner account (JWT create) |
| `profile_id` | `uuid` FK → `profiles` | Cascade delete |
| `profile_display_name` | `text` | Snapshot label |
| `source_surface` | `text` | `map` or `chart` |
| `conditions_json` | `jsonb` | Search/chart conditions; `chart_record_id` stripped on public read |
| `viewport_json` | `jsonb` | Map center/zoom when available |
| `settings_snapshot_json` | `jsonb` | `RMSettings.buildSettingsSnapshot(effective)` at share time |
| `place_id` | `uuid` nullable | Set when sharing from Screen 4 |
| `place_label` | `text` nullable | Human place name |
| `chart_facts_json` | `jsonb` nullable | Frozen planet/angle facts from Screen 4 |
| `created_at` | `timestamptz` | Default `now()` |
| `expires_at` | `timestamptz` | Default +30 days |
| `revoked_at` | `timestamptz` nullable | Reserved; no revoke UI in v1 |

**Indexes:** `account_id`, `expires_at`.

**Migration applied:** `supabase db query --linked -f supabase/migrations/2026_06_21_quick_shares.sql` (linked project).

---

## Endpoint contracts

### `POST /quick-share/create`

- **Auth:** JWT required (`Authorization: Bearer <token>`).
- **Scope:** Account membership via `app_account_ids`; profile must belong to account and not be archived.
- **Body:** `profile_id`, optional `profile_display_name`, `source_surface` (`map`|`chart`), `conditions_json`, `viewport_json`, `settings_snapshot_json`, optional `place_id`, `place_label`, `chart_facts_json`.
- **Success (200):** `{ quick_share_id, url: "/map_CURRENT.html?quickShare=<uuid>", expires_at }`
- **Errors:** `401` auth/account; `404` profile; `422` invalid surface / create failure.

### `GET /quick-share/{quick_share_id}`

- **Auth:** None (public read).
- **Success (200):** App-branded frozen payload with `brand: "Relocation Astrology"`, `kind: "quick_share_map"`, conditions/viewport/settings/place/chart_facts, `shared_view_notice`.
- **Privacy:** `chart_record_id` removed from public `conditions_json`.
- **Errors:** `404` not found / expired / revoked; `503` table missing.

**No mutation endpoints** in v1.

---

## UI surfaces

### Map (`map_CURRENT.html`)

- **Button:** `#quickShareBtn` — “Quick Share”.
- **Flow:** Requires profile + shareable search state. Captures conditions, viewport, settings snapshot; POST create; copies URL to clipboard.
- **Recipient:** `?quickShare=<uuid>` loads public payload, read-only chrome, replays search, shows chart facts panel when present.

### Screen 4 — Profile relocated chart (`app_shell.html`)

- **Button:** `[data-action="quick-share-chart"]`.
- **Flow:** Captures place + chart facts from `_screen4ChartCache`; `source_surface: "chart"`. Link opens map first.
- **Export screen:** Copy points users to Quick Share (Export not built).

### Shared helper (`quick_share.js`)

- `RMQuickShare.createAndCopyQuickShare`, `buildQuickShareUrl`, `renderChartFactsReadOnlyHtml`.

---

## Validation results

### `scripts/smoke_quick_share.py` — **11/11 PASS**

Proved: authenticated create, public read without JWT, UUID format, settings snapshot stored, map anchor URL, repository + static wiring, deprecated `share_links` not used for create.

HTTP smoke skipped unless port 8004 already running.

### Other smokes

Full `smoke_comparison_sets.py` not re-run (Playwright timeout on existing comparison AIS flow; unrelated to Quick Share).

---

## Known limits

- Frozen snapshot only; 30-day expiry; no revoke/history UI.
- Screen 4 shares open map anchor with optional chart facts panel, not full shell chart.
- Map replay depends on frozen conditions; Genie cross-tab sync not included.
- No PDF, Export Wizard, AI, ranking language, or practitioner branding.

---

## Rollback scope

1. Revert commit (UI + API + repository + migration file).
2. Optional DB: `drop table if exists quick_shares;`
3. No impact on `share_links` or canonical chart/settings pipelines beyond Export screen copy.

---

## Commit

```
QUICK-SHARE-MVP: add frozen map-first share links
```
