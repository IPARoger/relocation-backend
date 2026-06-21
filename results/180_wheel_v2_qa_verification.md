# WHEEL-v2-QA — P2P Spokes + Motion Markers Verification

**Date:** 2026-06-21  
**Type:** QA / verify only (no code changes)  
**Scope:** WHEEL-v2 commit `57e9d36` (+ backend deps P2P-ASPECTS-1, RETRO-MOTION-1)  
**Read:** `179`, `170`, `app_shell.html`, `main_centerline_FIXER.py`, `smoke_comparison_sets.py`

---

## Executive summary

**WHEEL-v2 is ACCEPTED** for relocated Screen 4 with canonical P2P spokes and motion markers.

Playwright QA across three live locations (Kansas City, Custom/NY, Moscow) confirms the wheel renders, draws 21 P2P chords matching `canonical_chart.aspects_planet_to_planet[]`, uses blue/red spoke colors per doctrine, shows retrograde (℞) and station-direct (`··`) markers aligned with `motion_state`, preserves AIS ASC/MC truth, and produces **zero console errors**. Minor quincunx spokes appear green/dashed when minors are enabled.

**Caveats (non-blocking):** `station_retrograde` glyph not exercised (no body in smoke birth at tested locations). Sun PIH house column shows angle-aspect labels near ASC at 2/3 sites (pre-existing PIH display; not a wheel regression). QA required restarting local `:8004` server — stale process lacked P2P/motion fields.

---

## Checklist results

| # | Check | Result | Evidence |
|---|--------|--------|----------|
| 1 | Wheel renders on Screen 4 | **PASS** | Playwright: `.rm-wheel-wrap[data-wheel-source="canonical_chart"]` at all 3 locations |
| 2 | P2P spokes from `aspects_planet_to_planet[]` | **PASS** | FE spoke count = backend row count (21/21) each site; `static_p2p_spokes_from_canonical` |
| 3 | No P2P table/grid | **PASS** | Headings: wheel → AIS → A2A → PIH only; `hasP2pTable=false` |
| 4 | Major harmonious spokes blue | **PASS** | `#2563eb` × 11 per location (trine/sextile rows) |
| 5 | Major challenging spokes red | **PASS** | `#dc2626` × 10 per location (conj/opp/square rows) |
| 6 | Minor spokes green/dashed when enabled | **PASS** | Settings patch: +1 green `#16a34a` dashed spoke; backend quincunx row matches |
| 7 | Retrograde markers where `motion_state=retrograde` | **PASS** | 2 ℞ glyphs ↔ Mars + Saturn at all 3 locations |
| 8 | Station markers for `station_direct` / `station_retrograde` | **PARTIAL** | 4 `··` markers ↔ Uranus, Neptune, Pluto, Chiron (`station_direct`). **No `station_retrograde` bodies in fixture** — glyph code present but not visually observed |
| 9 | Wheel matches AIS/PIH for ASC/MC and houses | **PARTIAL** | AIS ASC/MC **PASS** all 3. Sun house **PASS** Kansas City. Custom/Moscow PIH shows `Conjunction`/`Opposition` (near-ASC display) while canonical `Sun.house` is 12 / 7 — **pre-existing PIH quirk** (same as WHEEL-1 QA) |
| 10 | No console errors | **PASS** | `console_errors: []` in Playwright session |

---

## Static verification (`scripts/smoke_comparison_sets.py`)

All **17** checks **PASS** (`static_wheel_*`, `static_p2p_*`, `static_motion_*`).

---

## Manual QA — three locations

**Profile:** Smoke Renamed af11fd73  
**Birth:** 1976-01-13 (engine-birth)  
**Server:** `127.0.0.1:8004` (current codebase)

### 1. Kansas City, KS (current)

| Item | Value |
|------|-------|
| Screenshot | `results/180_wheel_v2_qa_screenshots/current_kansas_city.png` |
| P2P spokes (visible) | **21** (10 red, 11 blue) |
| Motion markers | ℞ ×2 (Mars, Saturn); `··` ×4 (Uranus, Neptune, Pluto, Chiron) |
| AIS ASC / MC | 8°09′ Capricorn / 1°24′ Scorpio — matches canonical |
| Sun PIH house | **1** — matches `canonical_chart.planets.Sun.house` |

### 2. Custom location (NY metro favorite)

| Item | Value |
|------|-------|
| Screenshot | `results/180_wheel_v2_qa_screenshots/favorite_city.png` |
| P2P spokes | **21** (10 red, 11 blue) |
| Motion markers | ℞ ×2; `··` ×4 |
| AIS ASC / MC | 29°16′ Capricorn / 22°17′ Scorpio — matches canonical |
| Sun PIH | Shows `Conjunction` (near ASC); canonical house **12** |

### 3. Moscow, Russia (comparison)

| Item | Value |
|------|-------|
| Screenshot | `results/180_wheel_v2_qa_screenshots/comparison_city.png` |
| P2P spokes | **21** (10 red, 11 blue) |
| Motion markers | ℞ ×2; `··` ×4 |
| AIS ASC / MC | 17°11′ Cancer / 9°58′ Pisces — matches canonical |
| Sun PIH | Shows `Opposition` (near ASC); canonical house **7** |

### Minors enabled (Kansas City)

| Item | Value |
|------|-------|
| Screenshot | `results/180_wheel_v2_qa_screenshots/current_kansas_city_minors_on.png` |
| Spokes | **23** total (+1 green dashed quincunx) |
| Backend | 23 P2P rows including 1 quincunx |

---

## Truth cross-checks

| Cross-check | Result |
|-------------|--------|
| Spoke count = `len(aspects_planet_to_planet)` | **PASS** (21 = 21, all 3) |
| Spoke colors ⊆ `{#2563eb, #dc2626, #16a34a}` | **PASS** |
| Retrograde glyph count = retrograde bodies | **PASS** (2) |
| Station-direct dot count = station_direct bodies | **PASS** (4) |
| Motion invariant across relocations | **PASS** |
| AIS formatted angles vs canonical | **PASS** (all 3) |
| No client P2P aspect math | **PASS** (static) |
| Section order meta → wheel → AIS → A2A → PIH | **PASS** |

---

## Visual issues (non-blocking)

1. **Spoke density** — 21 chords readable; may crowd at smaller viewports.
2. **Station vs retrograde** — `··` vs ℞ subtle but distinguishable; no legend (by design).
3. **Minimal SVG styling** — unchanged from WHEEL-1.
4. **`station_retrograde` ℞** — not visually verified (no fixture body).

No broken layout or color inversions observed.

---

## Truth mismatches

**None in wheel renderer paths.**

PIH Sun near-angle labeling at Custom/Moscow predates WHEEL-v2 (WHEEL-1 QA). Wheel tooltips use canonical `planets.Sun.house`.

---

## Ops note

Initial QA hit a **stale `:8004` process** (`p2p=0`, `motion_state=null`). After restart, fields populated. **Deploy must restart workers.**

---

## WHEEL-v2 acceptance

| Verdict | **ACCEPTED** |
|---------|----------------|
| Blockers | None |
| Follow-ups | `station_retrograde` spot-check; PIH near-angle display (separate) |

---

## Recommended next slice

**A2A-MOTION-1** — applying / separating / exact on `aspects_to_angles[]` (backend-first, per Phase 2B scoping).

Secondary: **natal wheel** (same renderer at birth location).

---

## Artifacts

| File | Purpose |
|------|---------|
| `results/180_wheel_v2_qa_verification.md` | This report |
| `results/180_wheel_v2_qa_data.json` | Machine-readable QA data |
| `results/180_wheel_v2_qa_screenshots/*.png` | Wheel captures (3 locations + minors) |

**No code changes. No commits.**

---

## Amendment (PIH-QA-FIX-1)

Checklist item 9 **Sun PIH** was **PARTIAL** due to a **QA selector bug** (not PIH display). See `181` / `182`.

| Location | Prior QA (wrong selector) | Corrected scoped PIH |
|----------|---------------------------|----------------------|
| Kansas City | 1 | **1** PASS |
| Custom/NY | Conjunction (A2A row) | **12** PASS |
| Moscow | Opposition (A2A row) | **7** PASS |

**WHEEL-v2 acceptance unchanged — ACCEPTED.**
