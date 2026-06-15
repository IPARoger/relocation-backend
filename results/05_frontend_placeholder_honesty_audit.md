# RESULT: 05_FRONTEND_PLACEHOLDER_HONESTY_AUDIT

Task: `05_FRONTEND_PLACEHOLDER_HONESTY_AUDIT`  
Mode: read-only audit; documentation output only  
Result: **VERIFIED**

## Telegram notifications

- Sent `started` exactly once at task start.
- Closeout notification will be sent after scope verification: `verified` if this result remains valid.
- No arbitrary text, task content, code, or paths were sent to Telegram.

## Files inspected

- `app_shell.html`
- `map_CURRENT.html`
- `account_drawer.js`
- `supabase_store_bridge.js`
- `docs/architecture/TWO_AGENT_RELAY_GOVERNANCE.md`
- `audits/01_backend_wiring_inventory.md`
- `audits/02_settings_consumption_audit.md`
- `audits/03_settings_truth_audit.md`

## Files changed by this task

Documentation / relay audit output only:

- `audits/05_frontend_placeholder_honesty_audit.md`
- `results/05_frontend_placeholder_honesty_audit.md`

No production app code was changed.

## Findings summary

Full inventory is in `audits/05_frontend_placeholder_honesty_audit.md`.

Highest-priority honesty risks found:

1. Stale saved-investigation replay copy still says saved conditions are not
   replayed, while current accepted behavior is replay + auto-search.
2. Export/share screen is reachable and shows an `https://example.com...` link,
   which looks like a share artifact but is not real share/export wiring.
3. In-shell `#/map` route remnants remain reachable through internal navigation
   and contain action buttons that can lead to missing-context states, even
   though primary Map nav now opens production `map_CURRENT.html`.
4. Screen 4 `Add to comparison` and `Back to map` labels imply stronger behavior
   than currently exists.
5. Production map city search is honestly labeled as a placeholder exact-name
   list, but remains a visible prototype-quality limitation.

Acceptable honest placeholders confirmed:

- Birth Data is read-only and explicitly says editing is not enabled.
- House-system Settings control is disabled and says Placidus only for now.
- Screen 4 and Comparison notes say placeholder / not saved.
- Map popup `Full chart coming soon` is disabled.
- Future rooms, AI/transit/Layer 4/5, debug/PoC map surfaces are clearly
  quarantined or debug-only.

## Rejected scope

- No code fixes.
- No backend/schema/database work.
- No Supabase writes or archive actions.
- No renderer/math/overlay investigation beyond reading visible map UI text in
  the authorized file.
- No export/share implementation.
- No notes implementation.
- No city/geocoder implementation.
- No task self-selection from the findings.

## Validation evidence

- Source/audit inspection completed for the exact authorized file list.
- `scripts/relay_notify.py started` returned `sent: started` once.
- Audit file written with findings and `VERIFIED` closeout.
- Scope check performed after writing outputs.

## Rollback

```
git checkout -- audits/05_frontend_placeholder_honesty_audit.md results/05_frontend_placeholder_honesty_audit.md
```

VERIFIED
