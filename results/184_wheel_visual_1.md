# WHEEL-VISUAL-1 — Beta Visual Language on Canonical WHEEL-v2

**Date:** 2026-06-21  
**Slice:** WHEEL-VISUAL-1  
**Status:** ACCEPTED  
**File changed:** `app_shell.html` (`renderRelocatedWheelSvg`, `.rm-wheel-disc` CSS)

---

## Goal

Recover approved beta wheel visual language from `relocated_standard.html` / `profile_standard.html` onto the canonical WHEEL-v2 renderer — **visual only**, no truth changes.

---

## Visual features recovered

| Feature | Source | Implementation |
|---------|--------|----------------|
| Warm paper base (`#eae8e3`) | beta `buildWheel` | SVG base rect |
| Zodiac band fill (`#f1ece0`) | beta | Stroke-width band between Rout/Rzod |
| Paper texture | beta `feTurbulence` | SVG filter @ 5% opacity |
| Inner radial glow | beta `#b89a55` α=0.16 | `radialGradient` @ 20% radius |
| Zodiac 30° dividers | beta | Ecliptic longitude → canvas |
| 5° degree tick ring | beta | Between Rzod and Rout |
| Zodiac glyph ring (12) | beta `wsign` paths | `wheelZodiacSignSvg()` |
| Alternating zodiac wedges | beta | Even 30° segments |
| Alternating house wedges | beta | Canonical `cusps_deg` |
| Ring hierarchy (4 rings) | beta | Rout / Rzod / Raring / Rcore |
| Warm grey palette | beta `GREY` | `WHEEL_GREY` constants |
| Plate/disc treatment | beta `.disc` CSS | `.rm-wheel-disc` box-shadow |
| Planet rim ticks | beta | Rzod + Raring ticks |
| Angle axis emphasis | beta | Thick lines cusps 1/4/7/10 |
| P2P spokes | WHEEL-v2 (unchanged) | `aspects_planet_to_planet` @ Raring |
| Motion markers | WHEEL-v2 (unchanged) | `motion_state` ℞ / ·· |
| Angle labels ASC/MC/DSC/IC | WHEEL-v2 (kept) | Warm blue `#3d6b86` |

### Screenshots

| Image | Description |
|-------|-------------|
| `results/184_wheel_visual_screenshots/after_wheel_visual_1.png` | Kyoto relocated wheel (canonical API) |
| User reference (2026-06-21) | Profile + Relocated beta mockup screenshots |

**Before:** WHEEL-v2 minimal — two grey circles, unicode glyphs, no atmosphere (see `results/180_wheel_v2_qa_verification.md`).

---

## Visual features intentionally deferred

- Stroke SVG planet glyphs (`wglyph`) — awaits GLYPH-SETTINGS-1
- Mockup spoke palette (`ASPCOL` earth tones) — WHEEL-v2 blue/red/green doctrine retained
- Popout / zoom affordance
- Natal wheel route
- Comparison multi-disc layout
- Rim degree labels, animation, typography/fonts
- Outer page `.disc.home/.guest` tint variants

---

## Glow / texture study archive (for review)

Studies comparing inner glow, outer glow, and texture tints:

| File | Focus |
|------|-------|
| `validation/mockups/beta/relocated_standard.html` | **Locked** wheel values: glow `#b89a55` α=0.16, paper filter, `.disc` shadow |
| `validation/mockups/beta/profile_standard.html` | Identical `buildWheel()` (natal plate) |
| `validation/mockups/beta/material_texture_study.html` | Linen/cotton/paper grain/letterpress/emboss/twill |
| `validation/mockups/beta/palette_study3.html` | Micro interior glow 3–5% |
| `validation/mockups/beta/palette_study4.html` | Teaching glow B (radial) vs C (inner-edge) |
| `validation/mockups/beta/palette_study5.html` | Live-with glow candidates |
| `validation/mockups/beta/shading_study.html` | Shading variants |
| `docs/design/visual_language_inventory_audit.md` | Doctrine index across mockups |

**WHEEL-VISUAL-1 used:** `relocated_standard.html` locked wheel params (not palette_study variants).

---

## Truth-path verification

### Static QA (all PASS)

```
static_wheel_source_attr, reads cusps/angles/planets/p2p/motion_state
static_wheel_no_client_aspect_math, no swe, no legacy geometry
static_motion_*, static_p2p_*
```

### Runtime (Kyoto relocated, canonical API)

| Check | Result |
|-------|--------|
| `feTurbulence` paper filter | PASS |
| `radialGradient` inner glow | PASS |
| `clipPath` disc mask | PASS |
| 12 zodiac stroke glyphs | PASS |
| House wedge fills from `cusps_deg` | PASS |
| P2P spoke count = `aspects_planet_to_planet.length` (24) | PASS |
| No `WHEEL_CUSPS` / `WHEEL_ASPECTS` in renderer | PASS |
| Motion markers present when `motion_state` set | PASS |

**Invariant:** All positions from `wheelEclipticToCanvasDeg(longitude, asc)` + `canonical_chart` only.

---

## Recommended next slice

**GLYPH-SETTINGS-1** — Curated glyph families (see `results/184_glyph_inventory_audit.md`), `resolveGlyph()` wired to wheel/tables/A2A/Ghost; optional stroke `wglyph` paths from mockup.

Alternative: **WHEEL-VISUAL-2** — mockup `ASPCOL` spoke palette as user setting (visual only).
