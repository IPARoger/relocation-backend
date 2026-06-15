# RESULT: 03_SETTINGS_TRUTH_AUDIT

**Author:** Cursor (results/ lane)
**Originating task:** tasks/03 settings truth audit (relay trial)
**Date:** 2026-06-15

## Files changed

None. Read-only audit.

## Files read

Inherits evidence from `audits/02_settings_consumption_audit.md`.
No additional source files needed.

## Findings summary

| Setting | Classification | MVP Required? | Action needed? |
|---|---|---|---|
| `default_chart_record_id` | MVP Product Truth | Yes | None — complete |
| `house_system` | Deferred Product Truth | No (if honest) | **Yes — UI honesty gap** |
| `zodiac_mode` | Deferred Product Truth | No | None |
| `orb_defaults` | Deferred Product Truth | No | None |
| `visible_minor_aspects` | Deferred Product Truth | No | None |
| `helper_layers` | Placeholder | No | None (review later) |
| `ontology_pack_id` | Abandoned (frozen) | No | None |
| `settings_version` | Placeholder | No | None |

**One actionable finding:** `house_system` is the only setting with a live
honesty gap. The UI shows a working dropdown and Save button; the engine ignores
it. This needs to be resolved before the app is presented to professional
astrologers — either by making the control honest ("Placidus only for now") or
by wiring the engine. The fix is in `app_shell.html` only (honesty path) or
`app_shell.html + main_centerline_FIXER.py + backend routes` (engine path).

## Validation evidence

All classifications based on evidence from audit 02 (E) and project governance
doctrine (E — governance docs in `docs/constitutional/` and `docs/product/`).
No new database queries. No files written beyond these two docs.

## Rollback procedure

```bash
rm -f audits/03_settings_truth_audit.md
rm -f results/03_settings_truth_audit.md
```

## Rejected scope

No implementations. No schema changes. No engine wiring. No self-selected
follow-up tasks.

## Remaining unknowns

- `helper_layers` intended use not confirmed from current files — observation
  only.

## Result

VERIFIED
