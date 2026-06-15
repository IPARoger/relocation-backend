# 06 Saved Investigation Replay Truth Audit

Task: `06_SAVED_INVESTIGATION_REPLAY_TRUTH_AUDIT`  
Mode: read-only audit; documentation output only  
Notification: `started` sent once via `scripts/relay_notify.py started`

## Scope

Authorized files read:

- `app_shell.html`
- `map_CURRENT.html`
- `supabase_store_bridge.js`
- `audits/05_frontend_placeholder_honesty_audit.md`
- `results/05_frontend_placeholder_honesty_audit.md`

No production code was modified. No database was read or written by this audit.

## 1. What Happens Today When A Saved Investigation Is Reopened

Current flow, source-backed:

1. `supabase_store_bridge.js` loads active, unarchived `saved_searches` rows for the account and maps them into `store.saved_investigations` with:
   - `id`
   - `client_id` / `profile_id`
   - `title`
   - `conditions_json`
   - `viewport_json`
   - `settings_snapshot_json`
   - `updated_at`

   Evidence: `supabase_store_bridge.js` lines 139-155 and 317-326.

2. `app_shell.html` adapts those rows into each Chart Record's `explorations` list. It formats condition labels for display and derives related `placeIds` only from favorite rows associated with that investigation.

   Evidence: `app_shell.html` lines 620-638.

3. The Dashboard and Chart Record Saved Explorations modules render `Resume → Map` buttons. The visible copy still comes from `RESUME_CONTEXT_STUB`.

   Evidence: `app_shell.html` lines 233, 931-933, 1103-1117, and 1185-1199.

4. Clicking `Resume → Map` in `app_shell.html` calls `openMap()` with:
   - `chartRecordId` from the clicked saved exploration's Chart Record
   - `explorationId` from the saved investigation row
   - `placeId` set to the first derived `exploration.placeIds[0]` if one exists, else `null`
   - source label `saved exploration → map`

   Evidence: `app_shell.html` lines 2015-2027.

5. `openMap()` builds a `map_CURRENT.html` URL with `handoff=app_shell`, `handoffCreatedAt`, and the populated nav context fields.

   Evidence: `app_shell.html` lines 780-848.

6. `map_CURRENT.html` reads the app-shell handoff from URL query params into `lastAppShellHandoff`, including `chartRecordId`, `placeId`, and `explorationId`.

   Evidence: `map_CURRENT.html` lines 979-1048.

7. On map load, `scheduleSupabaseSavedInvestigationReplay()` runs. It waits for chart profiles, fetches the saved investigation by `explorationId`, blocks archived/missing rows, account-mismatched rows, or fetch errors, applies saved conditions, applies saved viewport if valid, and then auto-runs `findRegions()` exactly once.

   Evidence: `map_CURRENT.html` lines 1830-1914, 1914-1945, and 6108-6124.

8. The auto-search step sets `#chartProfile` to the handoff `chartRecordId` before calling `findRegions()`.

   Evidence: `map_CURRENT.html` lines 1926-1935.

## 2. Files Owning This Behavior

| File | Ownership |
|---|---|
| `supabase_store_bridge.js` | Reads `saved_searches` into the app shell store and exposes saved investigation rows to the shell. |
| `app_shell.html` | Displays saved explorations, shows resume copy, builds map handoff URL, and passes `chartRecordId`, `explorationId`, and possible first `placeId`. |
| `map_CURRENT.html` | Receives handoff, fetches `saved_searches` by `explorationId`, applies conditions and viewport, selects profile/chart record, and auto-runs search once. |
| `audits/05...` / `results/05...` | Prior audit already identified stale replay copy as a high-priority honesty risk. |

## 3. What Is Restored

| Item | Restored? | Evidence / exact behavior |
|---|---:|---|
| Chart Record / profile | YES | `app_shell.html` passes `chartRecordId`; map reads it from handoff; auto-run sets `#chartProfile` to the handoff `chartRecordId` before `findRegions()` (`app_shell.html` lines 2015-2027; `map_CURRENT.html` lines 979-1048, 1926-1935). Birth resolution also falls back to the handoff `chartRecordId` (`map_CURRENT.html` lines 2076-2124). |
| Conditions: planet-in-house | YES | `applySavedInvestigationConditions()` restores slots A, B, C into `planetA/houseA`, `planetB/houseB`, `planetC/houseC`; missing B/C slots are cleared (`map_CURRENT.html` lines 1769-1797). |
| Conditions: angle-in-sign | YES | Restores the first `angle_sign_conditions[0]` into `angleSignAngle` and `angleSignSign`; clears `angleSignAngle` if absent (`map_CURRENT.html` lines 1798-1805). |
| Conditions: aspect overlay | YES | Restores `overlayPlanet`, `overlayAspect`, and `overlayAngle` from `aspect_overlay` (`map_CURRENT.html` lines 1806-1813). |
| Viewport center / zoom | YES | Fetches `viewport_json`, derives center/zoom, and calls `window.__rmMap.setView([center.lat, center.lon], zoom, { animate: false })` when valid (`map_CURRENT.html` lines 1896-1901). The legacy library replay path also applies center/zoom (`map_CURRENT.html` lines 1830-1847). |
| Search / overlays | YES, by rerun | After successful replay, `autoRunSavedInvestigationSearchOnce()` calls `findRegions()` one time (`map_CURRENT.html` lines 1914-1945). This regenerates current overlays from restored controls and current backend/renderer behavior. |
| Archived/missing/account-mismatched safety | YES | Replay fetch filters `archived_at IS NULL`, returns false for missing/archived rows, and checks `account_id` mismatch (`map_CURRENT.html` lines 1874-1889). |
| Place handoff | PARTIAL | Shell may pass the first derived `exploration.placeIds[0]` as `placeId` (`app_shell.html` lines 2015-2027), but replay explicitly skips `centerOnHandoffPlaceId()` when `explorationId` is present so viewport replay remains authoritative (`map_CURRENT.html` lines 6215-6222). |
| Settings snapshot | LOADED IN STORE, NOT RESTORED | Bridge maps `settings_snapshot_json` into `settings_snapshot` (`supabase_store_bridge.js` lines 317-326), and save writes `settings_snapshot_json: {}` (`map_CURRENT.html` lines 1702-1713). Replay fetch selects only `id, account_id, title, conditions_json, viewport_json, archived_at` and does not fetch or apply settings snapshot (`map_CURRENT.html` lines 1874-1879). |

## 4. What Is NOT Restored

- `settings_snapshot_json` is not applied. In current save path it is `{}`, and replay does not select it.
- Full map state is not restored as a serialized render artifact. The system restores controls + viewport and reruns `findRegions()`; it does not restore prior generated polygons/tiles/layers from storage.
- Bounds (`north/south/east/west`) are saved in `viewport_json`, but replay uses center + zoom only.
- `placeId` is not used to recenter during saved-investigation replay; that is intentionally skipped when `explorationId` exists so saved viewport wins.
- Popups, selected city/search field text, Saved Places dropdown selection, debug flags, onboarding dismissed state, and transient UI state are not restored.
- Comparison set context is not part of saved investigation replay.
- Future settings such as house system, zodiac mode, orb defaults, helper layers, minor aspects, and ontology pack are not applied from a saved snapshot.

## 5. Does Current UI Copy Accurately Describe Behavior?

No.

The active copy is:

> `Resume passes context only; saved conditions not replayed on map (v1).`

Evidence: `app_shell.html` line 233, rendered by `resumeContextStubHtml()` at lines 931-933 and shown near `Resume → Map` in Dashboard and Chart Record modules.

This is false against current code. Current code **does** replay saved conditions, applies viewport center/zoom when valid, selects the handoff chart record/profile before auto-search, and auto-runs `findRegions()` once.

Prior audit `05` already classified this as the top stale-copy honesty risk.

Evidence: `audits/05_frontend_placeholder_honesty_audit.md` lines 31-39 and 65-82; `results/05_frontend_placeholder_honesty_audit.md` lines 35-45.

## 6. Honesty Gaps

| Gap | Severity | Truth |
|---|---|---|
| Stale replay copy says conditions are not replayed | HIGH | Conditions are replayed and auto-search runs. |
| Copy says `context only` | HIGH | Replay also fetches saved row from Supabase, applies conditions, viewport, profile selection, and reruns search. |
| No user-facing precision about viewport | MEDIUM | Viewport center/zoom are restored if valid; bounds are saved but not directly applied. |
| Place behavior is implicit | MEDIUM | A possible `placeId` can be handed off, but saved-investigation replay gives priority to viewport and skips place recentering. |
| Settings snapshot is invisible/inert | LOW currently | It is stored in store shape but not meaningfully saved or replayed. No current UI claims otherwise. |
| “Map state” could be misunderstood | LOW currently | Actual behavior is rerun, not exact persisted overlay restoration. Existing copy does not claim exact map-state restoration. |

## 7. Correct Future Fix: Copy Change, Wiring Change, Or Both?

### Immediate honesty fix: copy change only

For the specific current UI dishonesty, the correct future fix is **copy change only**.

Reason: the workflow already restores materially more than the copy claims. The stale text should be replaced with truthful copy describing current behavior, e.g. conceptually:

- conditions restore
- saved viewport restores when available
- search auto-runs once
- archived/missing investigations do not replay

This audit does not implement that copy change.

### Optional future product work: wiring change only, if desired

If the product later wants stronger replay semantics, separate wiring tasks would be needed for:

- applying `settings_snapshot_json`
- deciding whether saved bounds matter beyond center/zoom
- restoring a specific selected place/popup independently of viewport
- persisting and replaying exact rendered map artifacts rather than rerunning search
- preserving transient UI state such as city search, drawer state, selected saved place, or debug flags

### Both

“Both” is only necessary if future UI copy is expanded to promise settings snapshot, exact full map state, or selected-place restoration. Current high-priority honesty problem does **not** require wiring; it requires truthful copy.

## Closeout

Files written by this task:

- `audits/06_saved_investigation_replay_truth_audit.md`
- `results/06_saved_investigation_replay_truth_audit.md`

No production code changed. No database action performed.

VERIFIED
