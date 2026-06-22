# 236 — Web2 Infrastructure Lockdown Audit

**Date:** 2026-06-23
**Task:** WEB2-INFRASTRUCTURE-LOCKDOWN-AUDIT-1
**Mode:** Audit only — no implementation
**Read budget used (8 files):**
1. `results/234_settings_live_wiring_audit.md`
2. `results/235_set4_profile_settings_propagation_closeout.md`
3. `app_shell.html` (targeted: auth methods, notes/favorites/comparison write paths, settings scope, rehydrate)
4. `auth.html` (targeted: auth methods, password reset)
5. `auth_guard.js` (full — small file)
6. `supabase_store_bridge.js` (targeted: RMSettings schema, buildSettingsSnapshot, store builder queries)
7. `user_profile.js` (targeted: ownership resolution)
8. (file 8 was not needed — stop rule not triggered)

---

## 1. Auth status

### Email / password
- **Sign-up:** `client.auth.signUp({ email, password })` — live, email confirmation required.
- **Sign-in:** `client.auth.signInWithPassword({ email, password })` — live.
- **Password reset:** `client.auth.resetPasswordForEmail(email, { redirectTo })` — live; confirmation message shown in UI: "Password reset email sent. Check your inbox."
- **Password show/hide toggle:** live in UI.
- **Verdict:** ✅ PASS

### Google OAuth
- No `signInWithOAuth({ provider: "google" })` call found in `auth.html`.
- No Google button exists in the auth UI HTML.
- **Verdict:** ❌ NOT IMPLEMENTED — absent from `auth.html`

### Apple OAuth
- No `signInWithOAuth({ provider: "apple" })` call found in `auth.html`.
- No Apple button exists in the auth UI HTML.
- **Verdict:** ❌ NOT IMPLEMENTED — absent from `auth.html`

### Session guard
- `auth_guard.js` runs `client.auth.getSession()` on every protected page load; redirects to `/auth.html` if no session.
- On Supabase CDN failure, redirects to auth as safe fallback (no silent page access).
- **Verdict:** ✅ PASS

---

## 2. User-owned object status table

### Legend
| Verdict | Meaning |
|---|---|
| PASS | Live, owned, writable, resumes correctly |
| PASS WITH WARNING | Works but with documented limitations |
| FAIL | Missing write path or ownership enforcement |
| NOT VERIFIED | No smoke test / no evidence of live path |

---

### Profiles (Chart Records)

| Dimension | Status |
|---|---|
| Source of truth | Supabase `chart_records` table |
| Read path | `supabase_store_bridge.js` → `buildSupabaseStore()` → `.eq("account_id", accountId)` |
| Write path | `POST /profiles/create`, `POST /profiles/archive` (with JWT) via `app_shell.html` |
| Ownership enforcement | `.eq("account_id", accountId)` on all reads; JWT required for writes |
| Replay/resume | Profile persisted in localStorage + `user_settings.default_chart_record_id`; resumes on reload |
| Smoke coverage | `smoke_profile_create.py`, `smoke_profile_rename_archive.py` (integration, require SUPABASE env) |
| Verdict | ✅ **PASS** |

---

### Favorites

| Dimension | Status |
|---|---|
| Source of truth | Supabase `favorites` table |
| Read path | `supabase_store_bridge.js` → `.select("id, profile_id, place_id, rank, label").eq("account_id", accountId)` |
| Write path | `POST /favorites/archive` (archive, with JWT); add favorite path lives in map page |
| Ownership enforcement | `.eq("account_id", accountId)` on reads; JWT on writes |
| Replay/resume | Loaded at store hydration; available as `r.favorites` on each chart record |
| Smoke coverage | `smoke_favorites.py` (integration) |
| Verdict | ⚠️ **PASS WITH WARNING** — archive write path in `app_shell.html`; add-favorite write path is in `map_CURRENT.html` (separate page). No in-shell add-favorite path confirmed. |

---

### Saved Investigations (Saved Searches)

| Dimension | Status |
|---|---|
| Source of truth | Supabase `saved_searches` table |
| Read path | `supabase_store_bridge.js` → `.select("id, profile_id, title, conditions_json, viewport_json, settings_snapshot_json, ...").eq("account_id", accountId)` |
| Write path | `POST /saved-searches/create` (with JWT, `profile_id`) from `app_shell.html` |
| Ownership enforcement | `.eq("account_id", accountId)` on reads; JWT on writes |
| Settings snapshot | `settings_snapshot_json` stored per row via `buildSettingsSnapshot()` at save time |
| Replay/resume | `conditions_json` + `viewport_json` sent to map for replay; smoke confirms `smoke_saved_investigations.py` |
| Smoke coverage | `smoke_saved_investigations.py` (integration) |
| Verdict | ✅ **PASS** — settings snapshot captured at save |

---

### Comparison Sets

| Dimension | Status |
|---|---|
| Source of truth | Supabase `comparison_sets` + `comparison_set_places` tables |
| Read path | `supabase_store_bridge.js` → `.eq("account_id", accountId)` with places join |
| Write path | `POST` + `PATCH` routes via `app_shell.html` (comparison workspace save) |
| Ownership enforcement | `.eq("account_id", accountId)` on reads; JWT on writes |
| Settings snapshot | `settings_snapshot_json` on `comparison_sets` row; populated via `buildSettingsSnapshot()` in chart transport |
| Replay/resume | Comparison workspace loads by `comparison_set_id`; places + settings snapshot re-applied |
| Smoke coverage | `smoke_comparison_sets.py` (integration, requires SUPABASE env) |
| Verdict | ✅ **PASS** — settings snapshot exists in schema |

---

### Notes

| Dimension | Status |
|---|---|
| Source of truth | Supabase `notes` table (`target_type` = `chart_record` or `comparison_set`) |
| Read path | `supabase_store_bridge.js` → `notes` query filtered by `account_id` + `archived_at IS NULL` + `target_type` |
| Write path (chart record notes) | `POST /notes/chart-record` with JWT; localStorage mirrored first as device fallback |
| Write path (comparison notes) | `POST /notes/comparison-set` with JWT; no localStorage fallback (account-only) |
| Ownership enforcement | Backend owns write; `account_id` passed via JWT; `profile_id` scopes per-profile |
| Fallback | Chart-record notes mirror to `localStorage("rm_note_<id>")` for offline/session-fail resilience |
| Replay/resume | `chartRecordInitialNote(r)` prefers account-backed note; falls back to localStorage |
| Smoke coverage | No dedicated `smoke_notes.py`; tested indirectly via comparison and profile smokes |
| Verdict | ⚠️ **PASS WITH WARNING** — no cross-device sync test; notes work requires active session; no dedicated smoke |

---

### Settings

| Dimension | Status |
|---|---|
| Source of truth | Supabase `user_settings` table, account-level row (`profile_id IS NULL`) |
| Read path | `supabase_store_bridge.js` → `.from("user_settings").eq("account_id", accountId).is("profile_id", null)` first row |
| Write path | `PATCH /settings/account` with JWT; shallow-merge into `settings_json` |
| Ownership enforcement | `.eq("account_id", accountId)` on reads; JWT on writes; backend enforces merge |
| Schema | `getEffectiveSettings()` in `supabase_store_bridge.js` — typed resolver with full default fallback chain |
| Snapshot | `buildSettingsSnapshot()` captures truth-relevant keys only; stored on `comparison_sets.settings_snapshot_json` and `saved_searches.settings_snapshot_json` |
| Propagation (Profile page) | Fixed in SET-4 (`bc6ac54`) — `rehydrateSettingsConsumers` now includes `"chart-record"` |
| Propagation (Relocated Chart, Comparison) | Live — cache cleared + re-hydrate triggered on settings save |
| Smoke coverage | `smoke_settings_account.py` (integration), `smoke_settings_navigation.py` (static + Playwright), `smoke_set4_profile_settings_propagation.py` (static) |
| Verdict | ✅ **PASS** — account-level scope, snapshot-at-save, three-route propagation now complete |

---

### Help

| Dimension | Status |
|---|---|
| Source of truth | Static content in `screenHelp()` in `app_shell.html` |
| Read path | Route `help` → `screenHelp()` → static HTML |
| Write path | None — read-only content |
| Ownership enforcement | N/A |
| Replay/resume | N/A — static |
| Smoke coverage | None |
| Verdict | ⚠️ **PASS WITH WARNING** — route exists and renders; content is minimal placeholder per roadmap ("Help content final (not placeholder)" listed as pre-beta item); no smoke |

---

## 3. Settings scope doctrine

### Current behavior: account-level defaults

Settings are stored in one `user_settings` row per account (`profile_id IS NULL`). All pages — Profile, Relocated Chart, Comparison — read the same effective settings via `_settingsEff()` → `getEffectiveSettings(raw.user_settings, null)`.

This means:
- A single change to `visible_planets` affects all Chart Records, all Relocated Charts, and all Comparison tables simultaneously.
- A single change to `house_proximity_orb_degrees` affects all near-cusp calculations across all pages.
- Changing `display_aspects_to_angles` toggles angle rows on every AIS/A2A table in the app.

### Retroactive rendering implications

**There are no frozen renders.** All page renders read settings at fetch time. If a user changes settings, **all pages immediately reflect the new values** on next hydration. Previously viewed charts are not preserved with their original settings unless a settings snapshot was attached at save time.

Saved Investigations and Comparison Sets **do** capture a `settings_snapshot_json` at save time via `buildSettingsSnapshot()`. However:
- This snapshot is **not currently used to restore settings on replay** — the replay path re-fetches with the current account-level settings, not the saved snapshot.
- The snapshot exists in the schema but is metadata-only for now.

### v2 per-profile / per-client settings room

The architecture **does leave room** for per-profile and per-client settings, but it is not yet implemented. Evidence:

1. **`getEffectiveSettings(storedUserSettings, ontologyDefaults)`** accepts an `ontologyDefaults` argument (second parameter). This seam is explicitly reserved for ontology packs. The same slot could serve per-profile overrides.
2. **`user_settings` has a `profile_id` column.** The store builder queries `profile_id IS NULL` for the account-level row, but the schema supports per-profile rows at `profile_id = <id>`. No code reads these yet.
3. **`settings_snapshot_json` on `comparison_sets` and `saved_searches`** is captured but not replayed — the replay infrastructure exists but the consumer side is not wired.

**This means the door is open, but:**
- Nothing in the current resolver (`getEffectiveSettings`) reads a per-profile row.
- No Settings UI exposes per-profile controls.
- Replay from snapshot is not implemented.

### Saved snapshot requirements (to avoid painting into a corner)

If replay-from-snapshot is added later, the following must hold:
1. `buildSettingsSnapshot()` must include all truth-relevant settings (it currently does: planets, bodies, aspects, orbs, house system, zodiac, proximity orb, etc.).
2. The snapshot must be passed to `getEffectiveSettings()` as `storedUserSettings` at replay time — the resolver is already shaped for this.
3. Renderer/display/cache state must **not** be in the snapshot (currently excluded by construction).
4. The snapshot version (`snapshot_version: 1`) allows forward migration when new fields are added.

### Architecture risks if ignored

| Risk | Severity |
|---|---|
| User changes orb settings after saving a comparison → replayed comparison shows different near-cusp results | **High** — silent truth change |
| Professional user manages multiple clients; changing one client's settings affects all | **High** — data bleed between clients (no per-profile isolation) |
| Saved Investigation replay re-renders with new aspect list, not original | **Medium** — investigation no longer reproducible |
| Two users share an account (e.g. family); one changes settings, breaks the other's charts | **Medium** — no user-level scoping |
| Per-profile house-system support requires a new resolver layer | **Low now** — the `profile_id` column and `ontologyDefaults` seam exist; wiring is additive |

**Recommendation:** Do not implement per-profile settings for Web2 beta. But add a one-sentence notice to the Settings page: "Settings apply to your whole account." This sets correct expectations and defers the isolation question cleanly.

---

## 4. Infrastructure blockers before Web2 beta

Ordered by user-visible severity:

| # | Blocker | Severity | Status |
|---|---|---|---|
| 1 | **Google / Apple login not implemented** | High | Auth UI only has email/password; no OAuth buttons or `signInWithOAuth` calls |
| 2 | **Help content is placeholder** | Medium | `screenHelp()` renders minimal static text; roadmap explicitly flags this pre-beta |
| 3 | **Subsequent house checkbox is interactive but non-functional** | Medium | Should be `disabled` (same pattern as House System, Zodiac) until policy calculation lands |
| 4 | **Major/minor aspect toggles not wired to chart tables** | Medium | Affect only Genie overlay; PIH/AIS/A2A tables show all aspects regardless |
| 5 | **A2A Comparison table stub** | Medium | `display_aspects_to_angles` and `aspect_to_angle_orbs` controls are live; primary consumer table is not rendered |
| 6 | **Notes: no dedicated smoke / no cross-device test** | Low | Notes write path exists but no `smoke_notes.py`; localStorage fallback could mask a silent backend failure |
| 7 | **Settings snapshot replay not wired** | Low | Snapshot captured at save; not consumed at replay. No truth regression today, but the gap will widen as more settings become live |
| 8 | **Map settings sync is load-time only** | Low | Genie sync runs on map load; settings changes in shell do not propagate without map reload |
| 9 | **No "settings apply to whole account" disclosure** | Low | Users with multiple Chart Records may be surprised by cross-profile settings bleed |

---

## 5. Explicit non-goals

The following are **out of scope** for Web2 beta and this audit:

- Color themes, typeface finalization, visual polish
- Map animation QA
- Diffs styling / information hierarchy implementation
- Per-profile settings implementation
- Per-comparison-set settings override
- Saved Investigation settings replay (snapshot exists; wiring is v3+)
- Advanced ontology packs / ontology-pack settings layering
- Multi-user / per-member settings isolation
- House system selection (requires engine change)
- Zodiac mode selection (requires engine change)
- North / South Node calculation

---

## 6. Recommended next 3 implementation slices

### Slice A: Subsequent house checkbox → disable (30 min)

**What:** Change the `subsequent_house_policy` checkbox from interactive to `disabled` with `title="Coming soon"`. Mirror the pattern already used for house system and zodiac mode. This eliminates a medium-severity false expectation with minimal risk.

**Files:** `app_shell.html` only (single attribute change in `subsequentHouseRuleHtml()`).
**Validation:** `node --check`; visual confirm in Settings → Astrology → Subsequent House Rule.
**Rollback:** Revert one line.

---

### Slice B: Rx / A/S markers on PIH and A2A rows (SET-1 start)

**What:** Add retrograde (ℛ) marker to planet name cells in PIH rows. Add applying/separating color class to A2A orb cells. Both are read from `canonical_chart.planets[name].motion_state` and `canonical_chart.aspects_to_angles[].applying` — already present in the canonical chart payload.

**Files:** `app_shell.html` — `formatTablePlanetNameHtml()` (Rx marker), `formatA2aOrbCellHtml()` (A/S class). CSS scoped to `#rm-profile-natal-facts`, `#rm-screen4-facts`, and comparison surfaces.
**Validation:** `smoke_rx_parity.py` (already exists); `smoke_profile_natal_wheel.py` regression.
**Rollback:** Revert `app_shell.html` inline CSS + marker HTML.

---

### Slice C: Notes smoke + account-level settings disclosure

**What:**
1. Write `scripts/smoke_notes_persistence.py` — static check that both note write paths exist, both fallback paths are documented, and `chartRecordInitialNote` prefers account note over localStorage.
2. Add one sentence to `settingsLandingHtml()` and `settingsChartsBodyHtml()`: "Settings apply to your whole account across all profiles."

**Files:** `scripts/smoke_notes_persistence.py` (new), `app_shell.html` (two small string additions).
**Validation:** `venv/bin/python scripts/smoke_notes_persistence.py`.
**Rollback:** Delete smoke; revert two `app_shell.html` lines.
