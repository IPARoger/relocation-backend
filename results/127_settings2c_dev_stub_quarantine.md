# SETTINGS-2C: Dev Stub Quarantine

**Date:** 2026-06-20  
**Scope:** `app_shell.html` (Settings UI only)  
**Doctrine:** `results/114_settings_doctrine_capture_v1.md`, `results/123_settings2_placeholder_audit_slices.md`

## Summary

Removed or quarantined developer-facing language from Settings. No persistence, backend, or layout redesign.

## Quarantined (removed from user view)

| Item | Action |
|------|--------|
| Effective configuration read-only panel | Removed from Astrology subpage (internal snapshot/ontology table) |
| Technical / Debug / Cache reset stubs | Removed dead `settingsTechnicalBodyHtml` |
| "S5 — Settings" screen label | → **Settings** |
| Implementation notes | Removed "not wired", "Layer 1/2", "engine-wired", "planned", "not configured" copy |
| Future Bodies label | → **More points** |
| Experimental location header | → Coming soon badge |
| Comparison reminders stub | Removed (out of doctrine scope for Notifications) |
| Dignity / interpretive hints dev notes | Replaced with product copy + Coming soon |

## User-facing copy retained

- **Coming soon** badges on unreleased controls (not banned; distinct from experimental/placeholder/dev)
- Functional astrology controls (bodies, aspects, orbs) with concise labels only
- Save Settings path unchanged

## Validation (2026-06-20, port 8004)

```
PASS: smoke_settings_navigation (16 checks)
PASS: smoke_settings_account (22 checks)
```

## Out of scope

- Wiring settings to calculation engine
- SETTINGS-2D astrology subsection reorder
- Removing `effectiveConfigPanelHtml()` function body (kept in file, not rendered)
