# Corrective UI / overlay QA pass (screenshot-driven)

Functional-only adjustments: **no astrology math** changes; **no global redesign**. Backend/search-regions semantics unchanged in this pass.

## Files touched

| File | Summary |
|------|---------|
| `map_CURRENT.html` | Fixed broken `#debugStatus` CSS block; **legend hidden** by default (`?debugGeometry` or `?showLegend`); **tighter panel** spacing; relocated popup **Planet/House** as **`<table>`** with bold headers; **QA-friendly onboarding skip** (`skipOnboarding`, `traceConditions`, `debugGeometry`, `showLegend`); consolidated **MAP_URL** flags. |
| `docs/overlay_and_aura_visual_strategy.md` | **§G** color/texture/mute semantics; **§H** layer-mute / mixer model; **§I** future map veil onboarding. |
| `validation/narratives/city_data_and_search_notes.md` | Geocoder **milestone** line (city/state/country/alt names). |
| `validation/narratives/overlay_truth_sanity_qa.md` | **Sidebar legend** visibility note. |
| *This file* | Jaggedness / truth / validation checklist |

## Math / backend

**Unchanged** in this pass (no edits to `truth_grid_engine`, APIs, or chart math).

## Cause of jagged / blocky polygon edges

Investigation (code + pipeline behavior):

1. **`generation_mode=truth_grid`**  
   Regions are built from a **discrete lat/lon grid** at **`truth_grid_resolution`** (degrees per cell; frontend often sends **0.75**).  
   Adjacent true cells are **merged into larger axis-aligned rectangles** (`merge_field_rectangles` / `merge_house_rectangles` in `truth_grid_engine.py`).  
   **Effect:** boundaries are **piecewise horizontal/vertical** at multiples of the grid step and merge geometry—**not** smooth astrological “curves.” This can look **very jagged or stair-stepped**, especially when zoomed in. **This is an honest representation of the discrete field**, not a Leaflet rendering bug.

2. **`generation_mode=contour`**  
   Boundaries come from **contours** on a sampled grid, then **`approximate_polygon`** (simplification). Jaggedness can still reflect **grid resolution** (`resolution` in request, often **1.5°** in the map) and contour stepping; simplification **reduces** vertex count but does not invent sub-grid detail.

3. **Rendering**  
   House polygons use **fill-only** (`stroke: false`), so edges are **raw coordinate jumps**, pixels alias cleanly—**no cosmetic edge softening** was added (would not fix truth).

4. **Coarse aspect pass**  
   Staged ASC overlay uses **coarse → medium → final** `aspect_resolution`; transient geometry can look rougher until **final** completes. That is **expected** for progressive refinement, not the same as house hex-grid jaggedness.

**Bottom line:** dominant “blocky” look on **truth_grid** is **merged rectangles on a coarse grid** + **zoom**. Finer `truth_grid_resolution` increases payload/cost; smoother *appearance* without changing the set needs a **truth-preserving** geometric strategy (documented only here).

## Overlay truth findings (methodology; no new engine proof in-repo)

Manual ambiguity (“too perfect” overlaps, Saturn/house confusion) should be triaged as:

| Hypothesis | How to check |
|------------|----------------|
| **Logic bug** | Right-click popup **`/relocated-chart`** table vs expected; compare to `?traceConditions` polygon `planet` / `house` / `condition_index`. |
| **Stale render** | Change a dropdown; **Find regions**; confirm `findRegions` clears **polygon + aspect** layers (it does at start of each run). Watch **render token** if rapid clicks. |
| **Color / overlap semantics** | Multiple translucent fills + purple angle-sign; see `docs/overlay_and_aura_visual_strategy.md` **§G**. |
| **Grid / merge geometry** | Boundaries look “synthetic” because they **are** rectilinear merges—popup truth still authoritative. |

**Conclusion for this pass:** no code change to truth-grid math; interpretability improvements are **docs + UI compression + popup table clarity**; future **mute/solo** layers would help dissection.

## Popup alignment

- **Planet** / **House** are **separate `<th>`** headers, **bold**.
- Body: planet **`td`** left, house **`td`** centered, **regular** weight planet names.
- No concatenated “PlanetHouse” string in markup.

## City / country

Still **no country** in `cities.js`; popups **do not guess**. See `validation/narratives/city_data_and_search_notes.md`.

## Documented for later (not built)

- Full **texture / hatch** system (only with flag + semantic review).
- **Layer mute / solo** UI (mixer model in strategy doc **§H**).
- **Map veil** first-run (strategy doc **§I**).
- **Truth-preserving** smoother outlines or finer grid (product/engine tradeoff).

## Manual validation checklist

- [ ] **Baseline / high-north / southern** (within ±65°): overlays + popups.
- [ ] **City** vs **custom right-click** popup parity (table + ASC/MC).
- [ ] **Aggressive pan** + **○ reset** (map stability preserved).
- [ ] **Overlap-heavy**: `?traceConditions` + popup at intersection.
- [ ] **Variable changes**: new **Find regions** → no **ghost** polygons/lines from prior run.
- [ ] **Dropdown** select stability (regression: prior fix path untouched).
- [ ] **Laptop viewport**: side panel **no scroll** or minimal; legend **off** unless `?showLegend` / `?debugGeometry`.
- [ ] **QA**: `?traceConditions` or `?debugGeometry` does **not** show onboarding toast unless desired.
