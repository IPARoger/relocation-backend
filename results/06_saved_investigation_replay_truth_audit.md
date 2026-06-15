# RESULT: 06_SAVED_INVESTIGATION_REPLAY_TRUTH_AUDIT

Task: `06_SAVED_INVESTIGATION_REPLAY_TRUTH_AUDIT`  
Mode: read-only audit; documentation output only  
Result: **VERIFIED**

## Telegram notifications

- Sent `started` exactly once at task start.
- Closeout notification will be sent after scope verification: `verified`.
- No arbitrary text, task content, code, or paths were sent to Telegram.

## Files inspected

- `app_shell.html`
- `map_CURRENT.html`
- `supabase_store_bridge.js`
- `audits/05_frontend_placeholder_honesty_audit.md`
- `results/05_frontend_placeholder_honesty_audit.md`

## Files changed by this task

Documentation / audit output only:

- `audits/06_saved_investigation_replay_truth_audit.md`
- `results/06_saved_investigation_replay_truth_audit.md`

No production app code was changed.

## Findings summary

Full audit is in `audits/06_saved_investigation_replay_truth_audit.md`.

Current reopen behavior:

- `app_shell.html` passes `chartRecordId`, `explorationId`, and sometimes first related `placeId` into a `map_CURRENT.html` handoff URL.
- `map_CURRENT.html` fetches the active, unarchived `saved_searches` row by `explorationId`.
- Conditions are restored into the map controls: planet-in-house slots A/B/C, first angle-sign condition, and aspect overlay controls.
- Viewport center/zoom are restored when valid.
- Chart/profile selection is set from the handoff `chartRecordId` before auto-search.
- `findRegions()` auto-runs once after successful replay.
- Archived, missing, or account-mismatched saved investigations do not replay.

What is not restored:

- `settings_snapshot_json` is not applied.
- Saved bounds are not directly applied beyond center/zoom.
- Exact prior generated map artifacts are not restored; the search is rerun.
- Place recentering is skipped when `explorationId` is present so replay viewport wins.
- Popups, city search text, debug flags, drawer/UI state, selected saved place, and comparison context are not restored.

Main honesty finding:

- Current shell copy says: `Resume passes context only; saved conditions not replayed on map (v1).`
- That copy is false. Current behavior replays conditions, viewport, chart/profile, and auto-searches once.

Future fix classification:

- Immediate honesty correction: **copy change only**.
- Optional future stronger replay semantics (settings snapshot, exact map artifact restoration, selected-place restoration): **wiring change only** if explicitly desired later.
- **Both** only if future UI copy promises those stronger semantics.

## Rejected scope

- No code edits.
- No database reads/writes.
- No backend/schema changes.
- No saved investigation replay implementation changes.
- No UI copy change performed in this task.
- No broad repo audit outside listed files.

## Validation evidence

- `scripts/relay_notify.py started` returned `sent: started` once.
- Source inspection traced the replay chain across the authorized files.
- Audit file written and ends with `VERIFIED`.
- Scope verification performed after writing outputs.

## Rollback

```
git checkout -- audits/06_saved_investigation_replay_truth_audit.md results/06_saved_investigation_replay_truth_audit.md
```

VERIFIED
