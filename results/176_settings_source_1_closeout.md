# SETTINGS-SOURCE-1 Closeout

**Date:** 2026-06-21  
**Type:** Implementation closeout  
**Scope:** Make Settings the Layer-1 source of truth for `canonical_chart` A2A compute

---

## Summary

Authenticated `/relocated-chart` now loads account `user_settings` and passes resolved effective settings into `build_canonical_chart_v1` and `_compute_aspects_to_angles`. `metadata.effective_settings` echoes the settings actually used. A single JSON registry backs Python defaults; the browser loads the same registry from `GET /settings/astrology-defaults`. Client-side A2A settings re-filtering was removed.

---

## Files changed

| File | Change |
|------|--------|
| `settings/astrology_settings_defaults.json` | **New** — single astrology defaults registry |
| `services/account_settings_resolver.py` | Load defaults from JSON; `aspect_to_angle_orb_limit()` helper |
| `services/chart_effective_settings.py` | **New** — JWT → account settings → effective settings for chart compute |
| `main_centerline_FIXER.py` | `GET /settings/astrology-defaults`; `/relocated-chart` uses `resolve_chart_effective_settings`; A2A orb from registry; map overlay orb fallback from registry |
| `supabase_store_bridge.js` | Fetch defaults from API; `display_aspects_to_angles` in `storeUserSettings`; `RMSettings.DEFAULTS` getter |
| `app_shell.html` | Auth header on chart fetch; `aspectsToAnglesForDisplay` replaces drift filter; re-hydrate chart/compare after settings save |
| `map_CURRENT.html` | Auth header on fallback `/relocated-chart` fetch |
| `scripts/smoke_settings_account.py` | Four `be_settings_source_*` + `be_astrology_defaults_endpoint` checks (before Playwright) |
| `scripts/smoke_comparison_sets.py` | `static_a2a_no_settings_refilter` |

---

## Settings now honored by Layer 1 (authenticated `/relocated-chart`)

| Setting | Effect |
|---------|--------|
| `aspect_to_angle_orbs` | `orb_limit_deg` + row inclusion in `aspects_to_angles[]` |
| `visible_major_aspects` | Which aspect types are computed |
| `display_aspects_to_angles` | Which angles (ASC/MC/DSC/IC) appear in A2A rows |
| `visible_planets` | Core body filter at compute |
| `visible_bodies` | Chiron filter at compute |
| `out_of_sign_aspects` | Sign-gate for A2A rows |
| `house_proximity_orb_degrees` | `near_cusp`, `houses.proximity_orb_deg` (from stored settings when authenticated) |

All of the above are echoed in `canonical_chart.metadata.effective_settings`.

---

## Settings still NOT honored by Layer 1

| Setting | Status |
|---------|--------|
| `major_aspect_orbs` / `minor_aspect_orbs` | Stored only — no P2P compute yet (P2P-ASPECTS-1) |
| `visible_minor_aspects` / `visible_minor_aspects_list` | No minor A2A / P2P yet |
| `subsequent_house_policy` | Stored only — no direction-aware house reassignment |
| `house_system` / `zodiac_mode` | Metadata echo only; engine remains Placidus tropical |
| Map `/search-regions` overlay | Uses registry default orbs when `max_orb` omitted — **not** user JWT settings yet |
| Retrograde / motion / applying-separating | Not in scope |

---

## Client drift removal

| Before | After |
|--------|-------|
| `filterA2aRowsForLocalSettings` re-applied angle/body/major/oos filters | `aspectsToAnglesForDisplay` — shape guard only |
| Chart fetch without auth | `relocatedChartRequestHeaders()` passes Bearer token when session exists |

**Remaining defensive behavior:** After settings save, Screen 4 / comparison re-hydrate via `hydrateRelocatedChart()` / `hydrateComparisonColumns()`. Without re-fetch, cached columns could still be stale until navigation.

**AIS / comparison angle rows** still filter `display_aspects_to_angles` client-side for display (angles are always present in `canonical_chart.angles`; filtering is presentation-only).

---

## Smoke / validation results

| Check | Result |
|-------|--------|
| Static `static_*` (19) | **PASS** |
| TestClient `/settings/astrology-defaults` | **PASS** |
| TestClient unauthenticated `/relocated-chart` + `metadata.effective_settings` | **PASS** |
| `_compute_aspects_to_angles` orb + display angle unit tests | **PASS** |
| `scripts/smoke_settings_account.py` `be_settings_source_*` | Runs **before** Playwright (requires Supabase + server on 8004) |
| Playwright settings UI | **Flake** (pre-existing `.settings-landing-grid` timeout) |

---

## Rollback scope

Revert SETTINGS-SOURCE-1 commit. Unauthenticated `/relocated-chart` behavior preserved (query `house_proximity_orb` + registry defaults). Client A2A drift filter can be restored from git history if needed.

---

*SETTINGS-SOURCE-1 complete.*
