# SETTINGS-2B: Profiles Under My Data

**Date:** 2026-06-20  
**Scope:** `app_shell.html`, `scripts/smoke_settings_navigation.py`, `scripts/smoke_settings_account.py`  
**Doctrine:** `results/114_settings_doctrine_capture_v1.md`, `results/123_settings2_placeholder_audit_slices.md`, `results/125_settings2a_terminology_alignment.md`

## Summary

Profile management relocated from **Account** to **My Data** per settings doctrine. No backend, persistence, or layout redesign — existing controls reused.

## Account (after)

- Identity only: account name, role/plan, sign-in/billing deferral to account drawer
- No default-profile select, no Manage Profiles link
- Save bar removed (nothing saveable on this subpage)

## My Data (after)

| Section | Content |
|---------|---------|
| **Profiles** | Default profile select (`#rm-settings-default-cr`), Manage Profiles → |
| **Saved Searches** | Stub row |
| **Saved Comparisons** | Stub row |
| **Archives** | Stub row |
| **History** | Clear actions (coming soon) |
| **Export My Data** | Stub row |

Save bar enabled on My Data for default-profile persistence (same `save-settings` path as before).

## Smoke updates

- Navigation: `#sec-account-identity` (account), `#sec-data-profiles` (My Data)
- Account smoke: default-profile round-trip uses `settingsSubpage: 'data'`

## Validation (2026-06-20, port 8004)

```
PASS: smoke_settings_navigation (16 checks)
PASS: smoke_settings_account (22 checks)
```

## Out of scope

- Deep links into saved searches / comparisons modules
- Moving Appearance map “Manage Profiles” shortcut (contextual to current location)
- SETTINGS-2C dev stub quarantine
