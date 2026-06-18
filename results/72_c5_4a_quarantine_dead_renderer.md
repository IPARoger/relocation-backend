# C5-4a — Quarantine Dead Renderer Items

**Roadmap ID:** C5-4a  
**Status:** VERIFIED  
**Date:** 2026-06-18

## Summary

`renderBellAuraBandsAroundLine()` quarantined; smoke passed.  
`CANONICAL_RENDERER_BRANCH_ACTIVE` **not quarantined** — C5-4 audit misclassified it as DEAD; grep shows a live read at line 2536 (production smoke telemetry). Per task hard stop, left unchanged. C5-4 audit should reclassify that constant as LIVE.

---

## 1. Caller Check Output

### renderBellAuraBandsAroundLine

```
$ grep -n "renderBellAuraBandsAroundLine" map_CURRENT.html
4676:function renderBellAuraBandsAroundLine(_feature, _color, _aspectKey) {
```

**Result:** Definition only. Zero call sites. **Quarantined.**

### CANONICAL_RENDERER_BRANCH_ACTIVE

```
$ grep -n "CANONICAL_RENDERER_BRANCH_ACTIVE" map_CURRENT.html
1058:const CANONICAL_RENDERER_BRANCH_ACTIVE = false;
2536:        canonicalRendererBranchActive: CANONICAL_RENDERER_BRANCH_ACTIVE,
```

**Result:** Read site at line 2536 (`canonicalRendererBranchActive` in production smoke object). Also consumed at line 2594 via `Boolean(smoke.canonicalRendererBranchActive)`.

**Hard stop — not quarantined.** Audit item 71 incorrectly listed this as DEAD.

---

## 2. Lines Quarantined

### renderBellAuraBandsAroundLine — QUARANTINED

```javascript
// QUARANTINED C5-4a — empty disabled function, no callers. Restore if renderer regression found.
/** Prototype aura bands disabled — see validation/narratives/map_current_qa_cleanup_pass.md */
function renderBellAuraBandsAroundLine(_feature, _color, _aspectKey) {
    // if (!aspectAuraMode) return;
}
```

### CANONICAL_RENDERER_BRANCH_ACTIVE — NOT TOUCHED

Unchanged at line 1058. Live telemetry read at 2536 blocks quarantine.

---

## 3. Smoke Result

```
$ set -a && source .env.staging && set +a
$ venv/bin/python scripts/smoke_map_current.py
{
  "overall_pass": true,
  "report": "validation/reports/map_current_smoke.json",
  "url": "http://127.0.0.1:8004/map_CURRENT.html?bust=1781762645&skipOnboarding=1"
}
exit code: 0
```

---

## 4. Status: VERIFIED

**Scope met:** Only truly dead renderer item (`renderBellAuraBandsAroundLine`) quarantined. Live constant correctly excluded per hard stop. Smoke green.

**Follow-up:** Reclassify `CANONICAL_RENDERER_BRANCH_ACTIVE` in C5-4 audit as LIVE (telemetry field). No further quarantine needed unless smoke object is refactored in a separate task.
