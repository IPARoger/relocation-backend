# C-UX-2 — Comparison Workspace State Contract

**Date:** 2026-06-18  
**Roadmap ID:** C-UX-2  
**Checkpoint:** 88c4789 → this slice

# Files Changed

| File | Change |
|------|--------|
| `repositories/account_comparison_sets_repository.py` | `update_comparison_set_state()` — JWT-owned snapshot write |
| `main_centerline_FIXER.py` | `POST /comparison-sets/state` |
| `supabase_store_bridge.js` | Load `settings_snapshot_json` into store |
| `app_shell.html` | Workspace state model, UI controls, debounced save, restore on open |
| `scripts/smoke_comparison_sets.py` | BE/FE workspace round-trip; temp server if state route missing |

# State Contract

Persisted under `comparison_sets.settings_snapshot_json`:

```json
{
  "comparison_workspace_state": {
    "schema_version": 1,
    "collapsed_sections": { "ais", "pih", "a2a", "city_intelligence", "notes": bool },
    "visible_sections": { ... },
    "active_angle_tab": "all|asc|mc|dsc|ic",
    "diffs_enabled": false,
    "dignities_enabled": false,
    "interpretive_hints_enabled": false,
    "hidden_place_ids": [],
    "column_order_place_ids": []
  }
}
```

`column_order_place_ids` mirrors `comparison_set_places.sort_order` when absent. Hidden IDs are visibility-only.

# Backend Route

**`POST /comparison-sets/state`** (new — no existing JWT route updated snapshots)

- Input: `profile_id`, `comparison_set_id`, `settings_snapshot_json`
- Updates: `settings_snapshot_json`, `updated_at` only
- Ownership: account + profile + non-archived set
- Does not revive deprecated `PATCH /comparison-set/{id}`

# Store/Bridge Changes

- Bridge selects `settings_snapshot_json` for comparison sets
- Store shape: `settings_snapshot_json` on each `comparison_sets` row
- View model: `workspaceState` normalized via `extractWorkspaceStateFromSnapshot()`

Existing fields preserved: `id`, `client_id`, `place_ids`, `notes`, etc.

# Restore Behavior

On open saved comparison (`screenCompare` with `comparisonSetId`):

- Merge DB snapshot with defaults
- Apply angle tab filter to facts table
- Apply collapsed/visible section UI
- Apply hidden place chips; visible columns use filtered `data-place-ids`
- `column_order_place_ids` from snapshot or DB place order

# Save Behavior

- Debounced save (700ms) on workspace UI changes
- `flushComparisonWorkspaceState()` exposed on `__rmAppShell` for smokes
- Create flow seeds default workspace state in memory
- Notes remain separate (`POST /notes/comparison-set`) — unchanged

# Unsupported/Future Keys

| Key | Status |
|-----|--------|
| `diffs_enabled` | Persisted; **not rendered** |
| `dignities_enabled` | Persisted; **not rendered** |
| `interpretive_hints_enabled` | Persisted; **not rendered** |
| Full AIS/PIH/A2A/City Intelligence tables | Placeholder section bodies only |
| Unified search (Family B) | **C-UX-3** — doctrine noted, not implemented |

# Validation

```bash
set -a && source .env.staging && set +a
venv/bin/python scripts/smoke_comparison_sets.py   # PASS 19/19
venv/bin/python scripts/smoke_map_current.py       # PASS
```

Workspace smokes: `be_state_200`, `fe_workspace_reload_tab`, `fe_workspace_reload_collapsed`, `fe_workspace_db_tab`

# C-UX-2 Verdict

**PASS** — Comparison workspace reading state persists via `settings_snapshot_json` and restores on reopen. Backend create/archive/notes/order unchanged. Ready for C-UX-3 unified search.
