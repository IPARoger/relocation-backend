# Map Current Aura Debug Smoke Split

## Status

Validation narrative for splitting aura debug checks out of the default `map_CURRENT.html` production smoke.

This is not production aura integration. It does not authorize a renderer substrate flip.

---

## Purpose

`scripts/smoke_map_current.py` is the default production map smoke. It should stay focused on catastrophic regressions in the normal `map_CURRENT.html` path:

- page load,
- profile/dropdown stability,
- default overlay generation,
- popup behavior,
- map bounds and zoom basics,
- console cleanliness,
- backend DC/IC validation,
- and the active default renderer substrate.

Raster/adaptive aura checks require debug query parameters and prototype API paths. Keeping those checks inside the default production smoke makes the smoke broader, slower, and easier to confuse with production aura integration.

---

## Split

Production/default smoke:

- `scripts/smoke_map_current.py`
- report: `validation/reports/map_current_smoke.json`

Aura debug/prototype smoke:

- `scripts/smoke_map_current_aura_debug.py`
- report: `validation/reports/map_current_aura_debug_smoke.json`

---

## Production Substrate Boundary

The active production substrate remains `legacy_search_regions`.

The default smoke verifies that the default map path is not using the canonical renderer branch, visible canonical debug mode, or canonical dry-run mode.

The aura debug smoke uses explicit debug flags:

- `?rasterAura=1&debugAura=1`
- `?debugAdaptive=1&debugAura=1`

These flags are prototype/debug validation surfaces. They are not evidence that aura is part of the default production renderer.

---

## Rollback Scope

Rollback is narrow:

- Revert the new aura debug smoke file if the prototype smoke becomes noisy.
- Revert the production smoke cleanup if the default smoke needs to temporarily carry broader coverage again.
- Revert the report files independently if only generated validation output needs regeneration.

No production UI, backend endpoint behavior, renderer implementation, truth-grid engine, Phase 2.25 path, scheduler/cache system, or aura implementation was changed by this split.

---

## Validation

Run:

```bash
./venv/bin/python scripts/smoke_map_current.py
./venv/bin/python scripts/smoke_map_current_aura_debug.py
```

Expected outputs:

- `validation/reports/map_current_smoke.json`
- `validation/reports/map_current_aura_debug_smoke.json`

The first report is production/default smoke evidence. The second report is debug/prototype aura evidence only.
