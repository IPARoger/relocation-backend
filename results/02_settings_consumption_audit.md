# RESULT: 02_SETTINGS_CONSUMPTION_AUDIT

**Author:** Cursor (results/ lane)
**Originating task:** tasks/02 settings consumption audit (relay trial)
**Date:** 2026-06-15

## Files changed

None. Read-only audit.

## Files read

- `supabase_store_bridge.js`
- `app_shell.html`
- `main_centerline_FIXER.py`
- `map_CURRENT.html`

## Findings summary

Eight fields live in `user_settings.settings_json`. Only one (`default_chart_record_id`)
actually affects runtime behavior.

| Setting | Has UI | Stored | Consumed | Status |
|---|---|---|---|---|
| default_chart_record_id | Yes | Yes | **Yes — dashboard/nav default** | Complete |
| house_system | Yes | Yes | **No — engine hardcodes Placidus** | Inert (honesty gap) |
| zodiac_mode | No | Yes | No | Inert |
| orb_defaults | No | Yes | No | Inert |
| visible_minor_aspects | No | Yes | No | Inert |
| helper_layers | No | Yes | No | Inert |
| ontology_pack_id | No | Yes | No | Inert (frozen layer) |
| settings_version | No | Yes | No active use | Placeholder |

**Critical:** `house_system` is the only user-visible inert setting. The engine
hardcodes Placidus (`b'P'`) in two places; the `/relocated-chart` route accepts
no house parameter; `SearchRequest` has no house field. User selects a setting
that never changes any calculation.

**Secondary finding:** `comparison_sets.settings_snapshot_json` is always
written as `{}` — settings are never snapshotted at comparison-build time.

## Validation evidence

- Hardcoded `b'P'` confirmed in `main_centerline_FIXER.py` lines 570 and 1791. (E)
- `relocated_chart()` signature: `lat, lon, birth_year, birth_month, birth_day,
  birth_hour_utc` — no house_system param. (E)
- `SearchRequest` model fields: no `house_system` field. (E)
- `supabase_store_bridge.js` loads `house_system` into store shape but it is
  not passed in any fetch call to the engine. (E)
- `comparison_sets` insert in `map_CURRENT.html`: `settings_snapshot_json: {}`. (E)
- No database queries performed; no files written beyond these two docs.

## Rollback procedure

```bash
rm -f audits/02_settings_consumption_audit.md
rm -f results/02_settings_consumption_audit.md
```

## Rejected scope

No code changes. No backend changes. No engine param threading. No schema changes.
No self-selected follow-up tasks. Findings are observations, not authorization.

## Remaining unknowns

- Whether `orb_defaults` were ever intentionally wired to any map overlay path
  (not visible in current files). Marked inference.

## Result

VERIFIED
