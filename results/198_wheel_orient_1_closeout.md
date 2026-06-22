# WHEEL-ORIENT-1 Closeout

**Date:** 2026-06-22  
**Scope:** Wheel ecliptic orientation only — match beta standard CCW longitude sweep. No color, glow, glyph, spoke, or chart-data changes.

**Inputs:** `results/185_wheel_visual_provenance_audit.md`, `results/180_wheel_v2_qa_verification.md`, `results/184_wheel_visual_1.md`, `app_shell.html`

---

## Summary

Fixed wheel orientation so **increasing ecliptic longitude moves counterclockwise** on the rim, matching `validation/mockups/beta/relocated_standard.html` (`wedgeEven` / `pt(a+R)` convention). **ASC remains on the left** via `WHEEL_ASC_ROTATION_DEG = 180`. All layers share the same transform (cusps, planets, spokes, zodiac band, angle labels).

---

## Changes (`app_shell.html` only)

| Change | Detail |
|--------|--------|
| `wheelEclipticToCanvasDeg` | `(asc - lon)` → **`(lon - asc)`** (normalized) |
| `wheelSvgWedgeEven` | New helper — beta `wedgeEven` increment sweep for zodiac alternating bands |
| Zodiac wedges | `wheelSvgWedgeEven` for 30° sign bands (was `wheelSvgWedgeCanvas`) |
| House wedges | Unchanged — `wheelSvgWedgeCanvas` (cusp decrement sweep) |

**Unchanged:** colors, glow, paper filter, glyphs, P2P spoke colors/count, motion markers, canonical data paths, `WHEEL_ASC_ROTATION_DEG`, house/planet/spoke rendering logic.

---

## Verification

| Check | Result |
|-------|--------|
| `python3 scripts/smoke_wheel_orient.py` | **8/8 PASS** |
| `static_wheel_checks` + `static_p2p_checks` | **14/14 PASS** |
| ASC on left (Moscow fixture) | ASC x < cx ✓ |
| CCW near ASC (+5° → +15°) | Δ ≈ 0.175 rad ✓ |
| CCW sign step (15° → 45°) | Δ ≈ π/6 ✓ |
| Spoke endpoints | Same `wheelEclipticToCanvasDeg` + `wheelPolarXY` as planet ticks (no spoke code change) |

### Screenshots (Moscow relocated, smoke birth 1976-01-13)

| File | Description |
|------|-------------|
| `results/198_wheel_orient_screenshots/before_moscow_wheel.png` | Pre-fix (`asc - lon`, zodiac `wedgeCusp`) |
| `results/198_wheel_orient_screenshots/after_moscow_wheel.png` | Post-fix (`lon - asc`, zodiac `wedgeEven`) |
| `results/198_wheel_orient_screenshots/*.svg` | SVG renders alongside PNGs |
| `results/198_wheel_orient_screenshots/manifest.json` | Capture metadata |

Captured via `scripts/capture_wheel_orient_screenshots.py` (canonical `/relocated-chart` + isolated `renderRelocatedWheelSvg`).

---

## Rollback scope

Revert WHEEL-ORIENT-1 commit. Restores `asc - lon` and single `wheelSvgWedgeCanvas` for zodiac bands. No schema or API impact.

---

## Commit

```
WHEEL-ORIENT-1: fix wheel ecliptic CCW orientation
```
