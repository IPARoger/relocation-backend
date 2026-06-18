# C5-4a — Quarantine Dead Renderer Items

**Roadmap ID:** C5-4a  
**Status:** NOT VERIFIED  
**Date:** 2026-06-18

## Summary

Partial completion. `renderBellAuraBandsAroundLine()` quarantined successfully; smoke passed.  
`CANONICAL_RENDERER_BRANCH_ACTIVE` **not quarantined** — hard stop: call site found at line 2536 (audit incorrectly classified as dead).

---

## 1. Caller Check Output

### renderBellAuraBandsAroundLine

```
$ grep -n "renderBellAuraBandsAroundLine" map_CURRENT.html
4675:function renderBellAuraBandsAroundLine(_feature, _color, _aspectKey) {
```

**Result:** Definition only (line 4675). Zero call sites. **Safe to quarantine.**

### CANONICAL_RENDERER_BRANCH_ACTIVE

```
$ grep -n "CANONICAL_RENDERER_BRANCH_ACTIVE" map_CURRENT.html
1058:const CANONICAL_RENDERER_BRANCH_ACTIVE = false;
2536:        canonicalRendererBranchActive: CANONICAL_RENDERER_BRANCH_ACTIVE,
```

**Result:** Call site at line 2536 (`canonicalRendererBranchActive` field in smoke/state object).  
Also consumed at line 2594: `canonicalRendererBranchActive: Boolean(smoke.canonicalRendererBranchActive)`.

**Hard stop triggered — NOT quarantined.**

---

## 2. Lines Quarantined

### renderBellAuraBandsAroundLine — QUARANTINED

**Before (lines 4674–4677):**
```javascript
/** Prototype aura bands disabled — see validation/narratives/map_current_qa_cleanup_pass.md */
function renderBellAuraBandsAroundLine(_feature, _color, _aspectKey) {
    if (!aspectAuraMode) return;
}
```

**After (lines 4674–4678):**
```javascript
// QUARANTINED C5-4a — empty disabled function, no callers. Restore if renderer regression found.
/** Prototype aura bands disabled — see validation/narratives/map_current_qa_cleanup_pass.md */
function renderBellAuraBandsAroundLine(_feature, _color, _aspectKey) {
    // if (!aspectAuraMode) return;
}
```

### CANONICAL_RENDERER_BRANCH_ACTIVE — NOT TOUCHED

**Before (line 1058):**
```javascript
const CANONICAL_RENDERER_BRANCH_ACTIVE = false;
```

**After:** Unchanged (call site at 2536 blocks quarantine per task hard stop).

---

## 3. Smoke Result

```
$ set -a && source .env.staging && set +a
$ venv/bin/python scripts/smoke_map_current.py
{
  "overall_pass": true,
  "report": ".../validation/reports/map_current_smoke.json",
  "url": "http://127.0.0.1:8004/map_CURRENT.html?bust=1781762409&skipOnboarding=1"
}
exit code: 0
```

---

## 4. Status: NOT VERIFIED

**Reason:** `CANONICAL_RENDERER_BRANCH_ACTIVE` has a read site (line 2536) contrary to C5-4 audit classification. Per task hard stop, that item was not quarantined. Full C5-4a objective (quarantine both items) not met.

**Action taken:** Only `renderBellAuraBandsAroundLine()` quarantined. No commit or push (VERIFIED gate not met).

**Follow-up:** Reclassify `CANONICAL_RENDERER_BRANCH_ACTIVE` in audit as LIVE (telemetry/smoke field). If quarantine still desired, remove or inline the smoke object reference first in a separate task.
