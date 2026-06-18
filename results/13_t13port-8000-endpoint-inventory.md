# RESULT: 13_T13PORT-8000-ENDPOINT-INVENTORY

**Task:** T13 — Inventory Port 8000 Endpoints and Map Hard Dependencies  
**Roadmap ID:** T13_1  
**Mode:** Read-only diagnosis; documentation output only  
**Date:** 2026-06-18

## Files changed

| File | Action |
|------|--------|
| `relay/T13_port8000_inventory.md` | Created — full inventory table and archaeology sweep |
| `results/13_t13port-8000-endpoint-inventory.md` | Created — this closeout |

No production code, backend routes, schema, or HTML/JS modified.

## Files read

- `map_CURRENT.html` (repo root; task spec said `frontend/map_CURRENT.html` — **no `frontend/` dir**)
- `app_shell.html`
- `main_centerline_FIXER.py`
- `docs/architecture/FEATURE_STATUS_BOARD.md` (§4 B-2)
- `docs/architecture/PRODUCTION_ACCEPTANCE_CHECKLIST.md` (§3.3, §3.4, §11.3)
- Sandbox/archaeology HTML and `sampling_cache_fetch_bridge_dev.js` (grep sweep)
- `archives/validation_2026-05-15/html_snapshots/map_CURRENT.html` (historical comparison)

## Findings summary

1. **Active production UI is already rewired off port 8000.** `map_CURRENT.html` sets `API_BASE = ''` and `LIBRARY_API_BASE = ""`; aura, relocated chart, aspect orb, screen-pixel-truth, library, and search-regions calls use **same-origin relative paths**. `app_shell.html` calls `/relocated-chart` relatively for Screen 4 and Screen 5.

2. **All B-2 endpoints exist on `main_centerline_FIXER.py`** (the 8004 Web2 server): `/aura-field`, `/aura-raster`, `/aura-raster-adaptive`, `/aspect-orb-at-point`, `/relocated-chart`, `/screen-pixel-truth`, `/chart-profiles`, `/library/state`.

3. **Hardcoded `127.0.0.1:8000` persists only in archaeology:** sandbox HTML (7 files), validation sandboxes (5), `Old File/` maps (4), one dev JS bridge, and archived May-2026 `map_CURRENT.html` snapshot. None are active production UI.

4. **B-2 register is stale.** Docs still claim five hardcoded port-8000 calls block aura and popup charts. Live code contradicts this; migration appears **frontend-complete** with backend routes colocated on 8004.

5. **PARTIAL (not port) gaps remain:** aura and aspect-orb endpoints are PoC-scoped (Sun conjunct ASC); aura failures still tend toward console-only errors.

## Validation evidence

| Check | Result |
|-------|--------|
| `grep -rn "127.0.0.1:8000" map_CURRENT.html app_shell.html` | **0 matches** |
| Repo-wide HTML/JS hardcoded 8000 (excl. node_modules, backups, archives, tmp) | **17 matches** — all sandbox/archaeology/dev |
| Backend route grep for aura/relocated/aspect-orb/screen-pixel/library | **All present** on `main_centerline_FIXER.py` |
| Every grep match represented in inventory table | **Yes** — see archaeology section in `relay/T13_port8000_inventory.md` |
| B-2 cross-check | **Documented drift** — code migrated; blocker text not updated |
| Live endpoint testing | **Not performed** (per task hard stop) |

## Rollback command

```bash
rm -f relay/T13_port8000_inventory.md results/13_t13port-8000-endpoint-inventory.md
```

## Rejected scope

- No code changes to HTML, JS, or backend
- No server restarts or live HTTP probing
- No architecture/router edits
- No deletions of legacy references
- No PR opened
- No updates to `FEATURE_STATUS_BOARD.md` or other architecture docs (observation only)

## Recommended next actions (for follow-on tasks, not executed here)

1. Human review: confirm 8004-only smoke for aura + popup chart paths.
2. Update B-2 and PRODUCTION_ACCEPTANCE_CHECKLIST §3.3–3.4 to reflect same-origin wiring.
3. Optional: user-visible error when aura POST fails (UX, not port migration).
4. Optional: quarantine or annotate sandbox files still pointing at 8000.

## Result

**NOT VERIFIED**

Diagnostic complete; inventory contradicts B-2's "hardcoded port 8000" framing for active UI. Human review recommended before treating port-8000 migration as remaining work.
