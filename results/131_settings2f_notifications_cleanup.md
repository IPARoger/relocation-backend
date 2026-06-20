# SETTINGS-2F: Notifications Cleanup

**Date:** 2026-06-20  
**Scope:** `app_shell.html`  
**Doctrine:** `results/114_settings_doctrine_capture_v1.md`, `results/123_settings2_placeholder_audit_slices.md`

## Summary

Notifications settings aligned to doctrine: travel/location alerts only — not comparison updates or generic SaaS email stubs.

## Removed

| Item | Reason |
|------|--------|
| Email digests | Generic SaaS placeholder; not doctrine focus |
| Product updates | Generic product-announcement stub |
| "Email and in-app alerts (coming soon)" | Misleading section framing |

## Retained (future stubs)

| Item | Notes |
|------|-------|
| **Road Trip Mode** | Continuous route-based location alerts |
| **Airplane Mode** | Offline / saved-location travel alerts |
| **Location change alerts** | Effective relocation context changes |

Each stub uses existing `settingsStubRow` + **Coming soon** badge. No backend or delivery system added.

## Copy updates

- Landing card desc: Road Trip, Airplane Mode, and location-change alerts
- Subpage subtitle: Travel modes and location-change alerts
- Subhead: Travel & location

## Validation (2026-06-20, port 8004)

```
PASS: smoke_settings_navigation (16 checks)
PASS: smoke_settings_account (22 checks)
```

## Out of scope

- Notification delivery infrastructure (SETTINGS-4E)
- Wiring Road Trip / Airplane modes
- Comparison or saved-work alert channels
