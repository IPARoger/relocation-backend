# GENIE-V7-REGRESSION-REPAIR-1 — Closeout

## Goal
Restore identity stamp (nameplate) positioning after regression introduced in commit `056840e`.

## CSS removed (map_SANDBOX_genie_v7.html)

Duplicate map-local override block (~L203–209):

```css
/* map-local override — do NOT edit identity_stamp.css */
.identity-stamp {
  --authority-col-width: 200px;
  transform: scale(0.88);
  transform-origin: top left;
  top: 72px;
}
```

## CSS restored (.zb-name .nm setup styles)

```css
-webkit-text-stroke: .4px rgba(70,84,94,.55);   /* was: 0 */
text-shadow: 0 1px 2px rgba(255,255,255,.9);   /* was: none */
```

## Kept (not reverted)
- `body.explore .identity-stamp:hover .zb-name .nm` hover rule (animation-related)
- Rail 280px, builder, np-stub, ghoststrip, FLIP motion, flySave opacity fix

## Positioning
`#plate` retains `authority-col-x authority-block-y`; positioning now comes from shared `identity_stamp.css` (no map-only `top` / `scale` overrides).

## Screenshots (1440×900, setup mode)
| | Path |
|---|---|
| Before (056840e regression) | `results/230_genie_v7_regression_repair_1_screenshots/before_setup.png` |
| After (repair) | `results/230_genie_v7_regression_repair_1_screenshots/after_setup.png` |

Plate `getBoundingClientRect().top`: **72px** (before) → **132px** (after). No overlap with Back/Forward/Pin controls after repair.

## Validation

| Check | Result |
|---|---|
| Nameplate does not overlap Back/Forward/Pin | **PASS** |
| Setup mode loads (HTTP 200, no console errors) | **PASS** |
| Explore mode loads | **PASS** |
| No console 404s | **PASS** |
| flySave `disk.style.opacity='0'` line intact | **PASS** |
| `authority-col-x` + `authority-block-y` on `#plate` | **PASS** |
